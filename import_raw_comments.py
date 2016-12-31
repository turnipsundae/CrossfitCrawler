from database_setup import Workout, Comment, User, Result, engine
from sqlalchemy.orm import sessionmaker

from cat2 import GENDER_RE0, AGE_RE0, HEIGHT_RE0, WEIGHT_RE0 

def setup_session():    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def scrub(session):
    raw_results = []
    results = []
    rx = session.query(Comment).filter(Comment.text.like(r"%rx%"))
    for r in rx:
        t = GENDER_RE0.findall(r.text)
        if t:
            gender = t[0][1]
            age = AGE_RE0.findall(t[0][2])
            height = HEIGHT_RE0.findall(t[0][2])
            weight = WEIGHT_RE0.findall(t[0][2])
            raw_results.append(t[0])
            results.append([r.text, gender, age, height, weight])
    return (raw_results, results)
