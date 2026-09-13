from __future__ import absolute_import

import os
import stat
import tempfile

import yaml


def _restrict_permissions(path, descriptor=None):
    """Use owner-only POSIX file permissions where the platform supports them."""
    if descriptor is not None and hasattr(os, "fchmod"):
        os.fchmod(descriptor, 0o600)
    elif os.name != "nt":
        os.chmod(path, 0o600)


def save_credentials(path, credentials):
    """Atomically write a YAML credential file with restrictive permissions."""
    directory = os.path.dirname(os.path.abspath(path))
    descriptor, temporary_path = tempfile.mkstemp(
        prefix=".pytumblr-", dir=directory
    )
    try:
        _restrict_permissions(temporary_path, descriptor)
        with os.fdopen(descriptor, "w") as stream:
            descriptor = None
            yaml.safe_dump(credentials, stream, default_flow_style=False)
            stream.flush()
            os.fsync(stream.fileno())
        getattr(os, "replace", os.rename)(temporary_path, path)
        _restrict_permissions(path)
    except Exception:
        if descriptor is not None:
            os.close(descriptor)
        try:
            os.unlink(temporary_path)
        except OSError:
            pass
        raise


def load_credentials(path):
    """Read a regular, owner-controlled YAML credential file safely."""
    if not hasattr(os, "O_NOFOLLOW") and os.path.islink(path):
        raise ValueError("credential file must not be a symbolic link")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    file_stat = os.fstat(descriptor)
    if not stat.S_ISREG(file_stat.st_mode):
        os.close(descriptor)
        raise ValueError("credential path must be a regular file")
    if hasattr(os, "getuid") and file_stat.st_uid != os.getuid():
        os.close(descriptor)
        raise ValueError("credential file must be owned by the current user")
    if file_stat.st_mode & 0o077:
        _restrict_permissions(path, descriptor)
    with os.fdopen(descriptor, "r") as stream:
        credentials = yaml.safe_load(stream)
    if not isinstance(credentials, dict):
        raise ValueError("credential file must contain a mapping")
    return credentials
