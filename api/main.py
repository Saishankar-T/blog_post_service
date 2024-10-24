from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, posts
from api.lib.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BLOG POST CRUD OPERATIONS",version="1.0.0")

# Mentions domains 
origins = [
    "http://localhost",           
    "http://localhost:3000",      
]

# CORS ENABLED
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"],            
)

# AUTHENTICATION Router
app.include_router(auth.router, prefix="/api/auth",tags=["AUTHENTICATION"])
# BLOG POSTS CRUD Router
app.include_router(posts.router, prefix="/api",tags=["BLOG POSTS"])
