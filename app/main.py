# from fastapi import FastAPI


#initiate the app
# app = FastAPI()


# create a simple route
# @app.get("/")
# def read_root():
#     return {"message": "Hello  this is an ecommerce API and it is live  "}


from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers import products,auth

# Lifespan events are the modern way to run startup code in FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables (if they don't exist)
    print("🚀 Starting up... Connecting to DB")
    create_db_and_tables()


    yield
    # Shutdown: (You can add cleanup code here if needed)
    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(products.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Hello! The E-Commerce API is alive! 🚀"}