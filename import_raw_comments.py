from database_setup import Workout, Comment, User, Result, engine
from sqlalchemy.orm import sessionmaker

from util import GENDER_RE, AGE_RE, HEIGHT_RE, WEIGHT_RE, UNITS_RE, RESULTS_RE

def setup_session():    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

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

def scrub(session):
    raw_results = []
    results = []
    rx = session.query(Comment).filter(Comment.text.like(r"%rx%"))
    for r in rx:
        t = GENDER_RE.search(r.text)
        if t:
            gender = t.group(1)
            # age = AGE_RE.findall(t[0][2])
            # if age:
            #     age = age[0]
            # else:
            #     age = None
            # height = HEIGHT_RE.findall(t[0][2])
            # # height = convert_to_ft_in(height)
            # weight = WEIGHT_RE.findall(t[0][2])
            # # weight = convert_to_lbs(weight)
            # raw_results.append(t[0])
            res = RESULTS_RE.search(r.text)
            if res:
                res = res.group(0)
            units = UNITS_RE.findall(str(r.workout))
            if units:
                units = units[0]
            else:
                units = None
            
            result = Result(workout_id = r.workout_id,
                            comment_id = r.id,
                            user_id = r.user_id,
                            gender = gender,
                            # age = age,
                            # height = str(convert_to_ft_in(height)),
                            # weight = convert_to_lbs(weight),
                            result = res,
                            score = 0,
                            units = units,
                            mods = "Rx")
            results.append(result)
    return (raw_results, results)

def add_results_to_db(results, session):
    session.bulk_save_objects(results)

sess = setup_session()
rr, r = scrub(sess)
for i in r[0:10]:
    print (i.comment_id, i.gender, i.result)
