import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

# 1. Pull the connection URL dynamically from your docker-compose environment variables
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "my_database"

# Dict to store the persistent database client across the application
db_client = {}

# 2. Manage the connection lifecycle (Startup and Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the Docker container boots up
    print(f"Connecting to MongoDB at: {MONGO_URL}")
    db_client["client"] = AsyncIOMotorClient(MONGO_URL)
    db_client["db"] = db_client["client"][DATABASE_NAME]
    
    yield  # The FastAPI application runs and handles requests here
    
    # This runs when you type 'docker compose down'
    print("Closing MongoDB connection...")
    db_client["client"].close()

# Helper function to easily grab the db database instance inside your routes
def get_db():
    return db_client.get("db")