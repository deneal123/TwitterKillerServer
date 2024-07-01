import base64
from datetime import datetime


def generate_token(userid: int) -> str:
    token_data = f"{userid}:{datetime.utcnow()}"
    return base64.b64encode(token_data.encode()).decode()
