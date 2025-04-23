from fastapi import FastAPI

from app.routes import candidates

app = FastAPI(title="Resume Processing API")

app.include_router(candidates.router, prefix="/api", tags=["Candidate Details"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
