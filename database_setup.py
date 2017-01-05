import os, sys

### Configuration
from sqlalchemy import Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


### Classes to represent tables
class Workout(Base):
  """Workout represents one WOD. May contain duplicates."""
  __tablename__ = 'workouts'

  id = Column(Integer, Sequence('workout_id_seq'), primary_key=True)
  title = Column(String)
  description = Column(String)
  comments = relationship("Comment")

  def __repr__(self):
    return "<Workout(title='%s', description='%s')>" % (self.title, self.description)


class Comment(Base):
  """Comments for each workout."""
  __tablename__ = 'comments'

  id = Column(Integer, Sequence('comment_id_seq'), primary_key=True)
  text = Column(String)
  workout_id = Column(Integer, ForeignKey('workouts.id'))
  workout = relationship("Workout")
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship("User")

  def __repr__(self):
    return "<Comment(text='%s')>" % (self.text)

class User(Base):
  """Users that leave comments for the workout."""
  __tablename__ = 'users'

  id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
  username = Column(String)

  def __repr__(self):
    return "<User(username='%s')>" % (self.username)

class Result(Base):
  """Result of a user performing a workout"""
  __tablename__ = 'results'

  id = Column(Integer, Sequence('result_id_seq'), primary_key=True)
  workout_id = Column(Integer, ForeignKey('workouts.id'))
  workout = relationship("Workout")
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship("User")
  gender = Column(String)
  age = Column(Integer)
  height = Column(String)
  weight = Column(Integer)
  result = Column(Integer)
  units = Column(String)
  mods = Column(String)

  def __repr__(self):
    return "<Result('%d %s')>" % (self.result, self.units)

# To drop a table, User.__table__.drop(engine)

### Insert at end of file ###
engine = create_engine('sqlite:///workouts.db', echo=False)
Base.metadata.create_all(engine)
