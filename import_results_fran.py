from database_setup import Workout, Comment, User, Result, engine
from sqlalchemy.orm import sessionmaker
from util import RESULTS_RE

def setup_session():    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_workouts_by_name(session, name):
    return session.query(Workout).filter(Workout.description.like("%{}%".format(name))).all()

sess = setup_session()

fran_workouts = get_workouts_by_name(sess, "fran")

# print (fran_workouts)

f1 = fran_workouts[0]

for c in f1.comments:
    m = RESULTS_RE.match(c.text)
    if m:
        print ("<ID='{}', text='{}'".format(c.id, m.group(1)))
