from fastapi import FastAPI
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
