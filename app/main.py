import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]  , # Or use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/')
def home():
    return {'geet': 'Thank You'}


app.include_router(router)
