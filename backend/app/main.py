# 

# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from app.routes.auth import router as auth_router
# from app.routes.user import u
from app.routes.user import router as user_router
from app.routes import mfa
from app.routes import auth

app.include_router(auth.router)

app = FastAPI(
    title="PMO Platform API",
    description="Project Management Office Platform with Super-admin, Admin, Users, Clients, MFA",
    version="1.0.0"
)

# ---------------------------
# CORS configuration
# ---------------------------
origins = [
    "*",  # For dev, allow all origins. Change in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Include routes
# ---------------------------
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(mfa.router)

# ---------------------------
# Root endpoint
# ---------------------------
@app.get("/")
def root():
    return {"message": "PMO API is running"}
