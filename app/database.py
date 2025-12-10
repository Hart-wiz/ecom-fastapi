from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os
from app.models.product import Product
from app.models.user import User

# 1. Load the environment variables from the .env file
load_dotenv()

# 2. Get the raw connection string
database_url = os.environ.get("DATABASE_URL")

# Safety Check: Ensure the URL was actually found
if not database_url:
    raise ValueError("❌ DATABASE_URL not found in .env file")

# 3. Create the Database Engine
# The 'engine' is the factory that creates connections.
# echo=True prints every SQL command to the terminal (Great for debugging!)
engine = create_engine(database_url, echo=True)

# 4. The Initialization Function
# We call this when the app starts to create tables if they don't exist yet.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 5. The Session Dependency
# This is a specific FastAPI pattern.
# When an API request comes in, we 'yield' (give) a database session.
# When the request is done, we automatically close the session to save resources.
def get_session():
    with Session(engine) as session:
        yield session