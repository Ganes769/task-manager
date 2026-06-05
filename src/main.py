from fastapi import FastAPI

from src.connection import get_db, lifespan  # Import from your connection.py

# Initialize FastAPI and pass the imported lifespan context
app = FastAPI(lifespan=lifespan)

# 3. Test Route to verify Docker networking is fully functioning
@app.get("/test-db")
async def test_mongodb_connection():
    try:
        # Use the helper function to grab the live database connection
        db = get_db()
        if db is None:
            return {"status": "Failed", "error": "Database client not initialized."}
            
        # Ping the database using a native MongoDB server command
        server_info = await db.command("serverStatus")
        return {
            "status": "Connected!",
            "message": "FastAPI successfully reached 'mongo-db' container via connection.py.",
            "version": server_info["version"]
        }
    except Exception as e:
        return {"status": "Failed", "error": str(e)}