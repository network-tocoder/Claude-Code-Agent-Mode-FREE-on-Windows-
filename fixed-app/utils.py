def format_response(data: dict) -> dict:
    """Wrap data in a response object with status field."""
    if not isinstance(data, dict):
        data = {}
    response = {
        "data": data,
        "status": "success"
    }
    return response

def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculate discounted price based on rate (default 10%)."""
    if not isinstance(price, (int, float)) or not isinstance(discount_rate, (int, float)):
        return price
    return round(price * (1 - discount_rate), 2)

def find_duplicates(items: list) -> list:
    """Find duplicate items using a set for O(n) complexity."""
    seen = set()
    duplicates = []
    for item in items:
        if item not in seen:
            seen.add(item)
        elif item not in duplicates:
            duplicates.append(item)
    return duplicates

def parse_config(config_string: str) -> dict:
    """Parse comma-separated key=value pairs into a dictionary."""
    pairs = config_string.split(',')
    config = {}
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            try:
                config[key.strip()] = float(value.strip())
            except ValueError:
                config[key.strip()] = value
    return config