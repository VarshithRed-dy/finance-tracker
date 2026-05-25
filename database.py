from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./finance_tracker.db" #sqlite:/// means "use SQLite, and the file is at this path." ./finance.db

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #engine is the connection to the database, check_same_thread = False allows multiple threads(parts of your app) to use the database at the same time.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #SessionLocal is a factory that creates a new database connection(session) for each request.

Base = declarative_base() #Base is the base class for all db models.

def get_db(): # This is a dependency function that provides a database session to each request
    db = SessionLocal()
    try:
        yield db # This yields the session to caller - the caller can use it to interact with the database
    finally:
        db.close() # This closes the session when the caller is done with it

