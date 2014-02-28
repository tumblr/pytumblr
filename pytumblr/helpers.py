def validate_params(valid_options, params):
    """
    Helps us validate the parameters for the request

    :param valid_options: a list of strings of valid options for the
                          api request
    :param params: a dict, the key-value store which we really only care about
                   the key which has tells us what the user is using for the
                   API request

    :returns: None or throws an exception if the validation fails
    """
    #crazy little if statement hanging by himself :(
    if not params:
        return

    #We only allow one version of the data parameter to be passed
    data_filter = ['data', 'source', 'external_url', 'embed']
    multiple_data = filter(lambda x: x in data_filter, params.keys())
    if len(multiple_data) > 1:
        raise Exception("You can't mix and match data parameters")

    #No bad fields which are not in valid options can pass
    disallowed_fields = filter(lambda x: x not in valid_options, params.keys())
    if disallowed_fields:
        field_strings = ",".join(disallowed_fields)
        raise Exception("%s are not allowed fields" % field_strings)

def validate_blogname(fn):
    """
    Decorator to validate the blogname and let you pass in a blogname like:
        client.blog_info('codingjester')
    or
        client.blog_info('codingjester.tumblr.com')
    or
        client.blog_info('blog.johnbunting.me')

    and query all the same blog.
    """
    def add_dot_tumblr(*args, **kwargs):
        if (len(args) > 1 and ("." not in args[1])):
            args = list(args)
            args[1] += ".tumblr.com"
        return fn(*args, **kwargs)
    return add_dot_tumblr
