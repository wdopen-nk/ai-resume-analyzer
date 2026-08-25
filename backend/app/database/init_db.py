from app.database.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.resume import Resume
from app.models.analysis import Analysis
from app.models.job_match import JobMatch


def init_db() -> None:
    Base.metadata.create_all(bind=engine)