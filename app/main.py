import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from app.api.v1.auth import router as router_v1
from app.api.v2.auth import router as router_v2

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for health check
@app.get("/")
def root():
    return {"status": "ok", "message": "Thank You"}

# Include API routers
app.include_router(router_v1, prefix="/api/v1")
app.include_router(router_v2, prefix="/api/v2")

# __main__ block only for local dev (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)
