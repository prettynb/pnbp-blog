import uuid 
import pnbp


# Add the JWT .env file (on/for server deployment): 
JWT_SECRET = uuid.uuid4().hex

with open('/apps/pnbp-blog/.env', 'w') as f:
    f.write(f"JWT_SECRET={JWT_SECRET}\nJWT_ALGO=HS256")


# Create the API user (on/for server deployment):
nb = pnbp.Notebook(NOTE_PATH="~/ubuntu/notes")
nb.create_api_user()

