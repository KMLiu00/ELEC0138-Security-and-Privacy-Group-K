import os
import secrets
from cryptography.fernet import Fernet

def generate_keys():
    # Generate secret keys
    flask_secret_key = secrets.token_hex(32)
    fernet_key = Fernet.generate_key().decode()

    # Environment variable contents
    env_content = f"""FLASK_SECRET_KEY={flask_secret_key}
FERNET_KEY={fernet_key}
DB_SERVER=kmlxhwcw.database.windows.net
DB_NAME=kmlxhwcw
DB_USERNAME=hachiin
DB_PASSWORD=20000904ABcd
"""

    # Define the path for the .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')

    # Write environment variables to .env file
    with open(env_path, 'w') as file:
        file.write(env_content)

    print(f"Environment variables have been generated and stored in {env_path}")

if __name__ == "__main__":
    generate_keys()
