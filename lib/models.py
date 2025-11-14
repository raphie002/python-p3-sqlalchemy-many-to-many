# lib/models.py
from sqlalchemy import create_engine, func # type: ignore
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData # type: ignore
from sqlalchemy.orm import relationship, backref # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Define the association table for User and Game (Many-to-Many)
user_game_association_table = Table(
    'user_games',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('game_id', ForeignKey('games.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # One-to-Many relationship with Review
    reviews = relationship('Review', backref=backref('user'))
    
    # Many-to-Many relationship with Game
    games = relationship('Game', secondary=user_game_association_table, back_populates='users')

    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'name={self.name})'

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())

    # One-to-Many relationship with Review
    reviews = relationship('Review', backref=backref('game'))
    
    # Many-to-Many relationship with User
    users = relationship('User', secondary=user_game_association_table, back_populates='games')

    def __repr__(self):
        return f'Game(id={self.id}, ' + \
            f'title={self.title}, ' + \
            f'platform={self.platform})'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    
    # Foreign key for Game (already present in the original code, but confirmed here)
    game_id = Column(Integer(), ForeignKey('games.id'))
    
    # Foreign key for User (new)
    user_id = Column(Integer(), ForeignKey('users.id'))

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'game_id={self.game_id})'
    