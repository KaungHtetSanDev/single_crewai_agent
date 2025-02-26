import os
from dotenv import load_dotenv
def get_openai_api_key():
    load_dotenv()
    return os.getenv('OPENAI_API_KEY')
