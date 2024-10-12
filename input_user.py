from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# تنظیمات قالب‌ها و فایل‌های استاتیک
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# روتر برای نمایش فرم HTML
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit_form/")
async def submit_form(name: str = Form(...), last_name: str = Form(...), phone: str = Form(...), city: str = Form(...)):
    # تبدیل اطلاعات فرم به دیکشنری
    user_data = UserInfo(name=name, last_name=last_name, phone=phone, city=city)
    result = await save_user(user_data)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("input_user:app", host="127.0.0.1", port=8000, reload=True)
