#No AI assistance used for creating this file
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import code_refactoring

app = FastAPI(
    title="AI Semantic Code Refactorer",
    description="An AI-powered code refactoring service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(code_refactoring.router)

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "message": "Welcome to AI Semantic Code Refactorer API",
            "status": "operational",
            "version": "1.0.0"
        }
    )

@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "version": "1.0.0"
        }
    ) 