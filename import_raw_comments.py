from database_setup import Workout, Comment, User, Result, engine
from sqlalchemy.orm import sessionmaker

from util import GENDER_RE, AGE_RE, HEIGHT_RE, WEIGHT_RE 

def setup_session():    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def scrub(session):
    raw_results = []
    results = []
    rx = session.query(Comment).filter(Comment.text.like(r"%rx%"))
    for r in rx:
        t = GENDER_RE.findall(r.text)
        if t:
            gender = t[0][1]
            age = AGE_RE.findall(t[0][2])
            height = HEIGHT_RE.findall(t[0][2])
            weight = WEIGHT_RE.findall(t[0][2])
            raw_results.append(t[0])
            results.append([r.text, gender, age, height, weight])
    return (raw_results, results)

def convert_to_ft_in(height_param):
    # height_param is a tuple inside an array
    # 
    if not height_param:
        return None
    else:
        height_param = height_param[0]
        feet, inches, only_inches, cm  = height_param
        CM_PER_INCH = 2.54
        if only_inches:
            return divmod(int(only_inches), 12)
        elif cm:
            return divmod(int(cm) / CM_PER_INCH, 12) 
        elif feet and inches:
            return (int(feet), int(inches))
        elif feet:
            return (int(feet), 0)
        else:
            return None

def convert_to_lbs(weight_param):
    if not weight_param:
        return None
    else:
        weight_param = weight_param[0]
        lbs, kgs = weight_param
        LB_PER_KG = 2.20462
        if kgs:
            return (int(kgs.split('.')[0]) * LB_PER_KG)
        else:
            return int(lbs.split('.')[0])

# for i in range(6,16):
#     print (results[i][0])
#     print ("****************")
#     print (convert_to_ft_in(results[i][3]))
#     print (convert_to_lbs(results[i][4]))
#     print ("----------------")
