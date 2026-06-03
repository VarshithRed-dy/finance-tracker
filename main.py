import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from database import Base, engine, get_db
from routers import users, transactions, analytics

Base.metadata.create_all(bind=engine) #This looks at every class that inherits from Base(models) and creates the corresponding tables if they don't exist.

app = FastAPI(title="Personal Finance Tracker")

app.include_router(users.router) #Include router plugs each router into the app. Each router contains its own set of endpoints.
app.include_router(transactions.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Personal Finance Tracker API"}

logger = logging.getLogger("uvicorn.error")

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(f"Unhandled error at {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )