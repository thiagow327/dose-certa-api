from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db import db
from model.remedio import Remedio
from model.dose import Dose

engine = create_engine("sqlite://database/dose_certa.db", echo=True)
Session = sessionmaker(bind=engine)
