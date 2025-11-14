#!/usr/bin/env python3
# lib/debug.py
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

from models import Game, Review, User

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///many_to_many.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    import ipdb; ipdb.set_trace() # type: ignore
