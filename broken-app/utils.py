def format_response(data):
    if data == None:
        return {}
    response = {
        "data": data,
        "status": "success"
    }
    return response

def calculate_discount(price, discount_rate):
    discounted = price * (1 - discount_rate)
    return discounted

def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                if items[i] not in duplicates:
                    duplicates.append(items[i])
    return duplicates

def parse_config(config_string):
    pairs = config_string.split(',')
    config = {}
    for pair in pairs:
        key, value = pair.split('=')
        config[key] = value
    return config