from database.db import Base, engine, Session
from model.remedio import Remedio
from model.dose import Dose

Base.metadata.create_all(engine)