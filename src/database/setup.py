from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://root:haslo@db:6543/cinema"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@127.0.0.1:6543/academy"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)