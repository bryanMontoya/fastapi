from jwt import encode, decode

def create_token(data: dict):
    token: str = encode(payload = data, key = "my_string_key", algorithm = "HS256")
    return token

def validate_token(token: str) -> dict:
    return decode(token, key = "my_string_key", algorithms = ["HS256"])

