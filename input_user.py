from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

try:
    # تنظیمات اتصال به دیتابیس MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["mydatabase"]
    collection = db["user_info"]
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# مدل Pydantic برای ورودی‌ها
class UserInfo(BaseModel):
    name: str
    last_name: str
    phone: str
    city: str

@app.post("/save_user/")
async def save_user(user_data: UserInfo):
    try:
        # تبدیل ورودی‌ها به دیکشنری
        user_dict = user_data.dict()
        # ذخیره در دیتابیس
        result = await collection.insert_one(user_dict)
        return {"status": "Success", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error inserting document: {e}")
        return {"status": "Failed", "reason": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("input_user:app", host="127.0.0.1", port=8000, reload=True)
