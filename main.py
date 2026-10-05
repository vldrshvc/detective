from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, Mapped, mapped_column
from pydantic import BaseModel, ConfigDict

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_watcher(id, db):
    watcher = db.get(Watcher, id)
    if watcher is None:
        raise HTTPException(status_code=404, detail='Not Found')
    return watcher


class Base(DeclarativeBase):
    pass


class Watcher(Base):
    __tablename__ = "watchers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    url: Mapped[str]
    interval_minutes: Mapped[int] = mapped_column(default=60)
    is_active: Mapped[bool] = mapped_column(default=True)


class WatcherCreate(BaseModel):
    name: str
    url: str
    interval_minutes: int = 60
    is_active: bool = True


class WatcherRead(WatcherCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


Base.metadata.create_all(engine)

app = FastAPI()


@app.get('/')
def root():
    return {'status': 'ok'}


@app.post('/watchers', response_model=WatcherRead)
def add_watcher(data: WatcherCreate, db: Session = Depends(get_db)):
    watcher = Watcher(**data.model_dump())
    db.add(watcher)
    db.commit()
    db.refresh(watcher)
    return watcher


@app.get('/watchers', response_model=list[WatcherRead])
def read_watchers(db: Session = Depends(get_db)):
    return db.scalars(select(Watcher)).all()


@app.get('/watchers/{id}', response_model=WatcherRead)
def read_watcher(id: int, db: Session = Depends(get_db)):
    watcher = check_watcher(id, db)
    return watcher


@app.put('/watchers/{id}', response_model=WatcherRead)
def edit_watcher(id: int, data: WatcherCreate, db: Session = Depends(get_db)):
    watcher = check_watcher(id, db)
    for k, v in data.model_dump().items():
        setattr(watcher, k, v)
    db.commit()
    db.refresh(watcher)
    return watcher


@app.delete('/watchers/{id}', status_code=204)
def delete_watcher(id: int, db: Session = Depends(get_db)):
    watcher = check_watcher(id, db)
    db.delete(watcher)
    db.commit()
    return
