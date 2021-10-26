def check_attributes(object, attributes):
    return not list(set(attributes) - set(object.keys()))