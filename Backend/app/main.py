from fastapi import FastAPI

app = FastAPI(
    title="Hirly API",
    description="Agentic AI Recruitment System",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Hirly",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }