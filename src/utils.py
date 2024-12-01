import os
from dotenv import load_dotenv
from typing import Literal


load_dotenv()


PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

def update_env_variable(provider: Literal['groq', 'google'] = 'groq'):
    # dotenv path
    dotenv_path = os.path.join(PROJECT_DIR, ".env")
    
    # key's name pattern
    key = provider.upper() + "_API_KEY"
    
    # Read all the lines from the .env file
    with open(dotenv_path, 'r') as file:
        lines = file.readlines()

    # Find the current value of the key
    current_value = os.getenv(key)
    
    # Incremental check for keys (key1, key2, etc.)
    idx = 1
    while True:
        next_key = f"{key}{idx}"
        next_value = os.getenv(next_key)
        if current_value == next_value:
            break

        idx += 1

    next_value = os.getenv(f"{key}{idx + 1}") or os.getenv(f"{key}1")

    # Check if the key exists and update it
    with open(dotenv_path, 'w') as file:
        key_found = False
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}={next_value}\n")
                key_found = True
            else:
                file.write(line)

    # Reload the environment variables
    load_dotenv(dotenv_path, override=True)