from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="AI Semantic Code Refactorer",
    description="An AI-powered code refactoring service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return JSONResponse(
        content={
            "message": "Welcome to AI Semantic Code Refactorer API",
            "status": "operational",
            "version": "1.0.0"
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": "1.0.0"
        }
    ) 