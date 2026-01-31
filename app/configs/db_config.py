import os
from typing import Annotated, AsyncIterator
from dotenv import load_dotenv
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.configs.log_config import setup_logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


setup_logger()
load_dotenv()

# PostgreSQL Configuration (Commented out - using MySQL only)
# DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_ASYNC_URL = os.getenv("DATABASE_ASYNC_URL")
# Base = declarative_base()

# async_engine = create_async_engine(DATABASE_ASYNC_URL, echo=True, future=True)
# async_session = async_sessionmaker(
#     bind=async_engine,
#     autoflush=False,
#     future=True,
#     expire_on_commit=False
# )

# async def get_async_db() -> AsyncIterator[async_sessionmaker]:
#     try:
#         yield async_session()
#     except SQLAlchemyError as e:
#         logger.exception(e)


# engine = create_engine(DATABASE_URL)

# logger.info("Creating session local")
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# logger.info("Creating declarative base")
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



# MySQL Configuration for Realty Database
# Build connection URL from individual environment variables
import urllib.parse

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# URL encode the password to handle special characters like @, #, etc.
encoded_password = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else ""

MYSQL_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger.info(f"Creating MySQL engine for {DB_HOST}:{DB_PORT}/{DB_NAME}")
mysql_engine = create_engine(MYSQL_DATABASE_URL, echo=True, pool_pre_ping=True)

logger.info("Creating MySQL session local")
MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

logger.info("Creating MySQL declarative base")
MySQLBase = declarative_base()

def get_mysql_db():
    db = MySQLSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Make MySQL the default database for existing code compatibility
SessionLocal = MySQLSessionLocal
Base = MySQLBase
get_db = get_mysql_db

# Stub for get_async_db (not used with MySQL, but needed for imports)
async def get_async_db():
    raise NotImplementedError("Async database operations not available with MySQL. Use get_mysql_db() instead.")