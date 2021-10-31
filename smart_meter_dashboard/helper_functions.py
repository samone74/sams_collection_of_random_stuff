
def list2dict(input_list, values=None):
    if values is None:
        values = input_list
    ret_dict = [{'label': str(label), 'value': value} for label, value in zip(input_list, values)]
    return ret_dict
