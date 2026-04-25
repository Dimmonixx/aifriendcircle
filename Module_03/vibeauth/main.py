from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import hashlib

app = FastAPI(title="VibeAuth API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for users
users_db: List[Dict] = []

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    email: str

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/")
async def root():
    """Root endpoint - API status check"""
    return {"message": "VibeAuth API \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442!"}

@app.post("/register")
async def register(user: UserRegister):
    """Register a new user"""
    # Check if user already exists
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Create new user
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)
    }
    
    users_db.append(new_user)
    
    return {
        "message": "\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0441\u043e\u0437\u0434\u0430\u043d",
        "user": user.email
    }

@app.post("/login")
async def login(user: UserLogin):
    """Login user"""
    # Find user by email
    found_user = None
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            found_user = existing_user
            break
    
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check password
    if found_user["password"] != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return {"message": "\u0412\u0445\u043e\u0434 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d"}

@app.get("/users")
async def get_users():
    """Get all users without passwords"""
    users_without_passwords = []
    for user in users_db:
        users_without_passwords.append({
            "name": user["name"],
            "email": user["email"]
        })
    
    return {"users": users_without_passwords}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
