def toNamedTuple(data_class, dict_data):
    key_values = [dict_data.get(key) for key in data_class._fields]
    return data_class._make(key_values)