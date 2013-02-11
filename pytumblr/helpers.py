def validate_params(valid_options, params):
    
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
        raise Exception("You had a field which was disallowed")
    
