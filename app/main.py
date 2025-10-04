import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router
from app.api.v2.auth import router as routerv2

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
    return {'greetings': 'Thank You'}


app.include_router(router, prefix="/api/v1")
app.include_router(routerv2, prefix="/api/v2")


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)