from database_setup import Workout, Comment, User, Result, engine
from sqlalchemy.orm import sessionmaker

from util import GENDER_RE, AGE_RE, HEIGHT_RE, WEIGHT_RE, UNITS_RE, RESULTS_RE

import re

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
    results = []
    rx = session.query(Comment).all()
    for r in rx:

        gender = GENDER_RE.search(r.text)
        if gender:
            gender = gender.group(1)

        age = AGE_RE.search(r.text)
        if age:
            age = age.group(1)

        height = HEIGHT_RE.search(r.text)
        if height:
            i = height.lastindex
            h = height.group(i)
            if i > 1:
                CM_PER_INCH = 2.54
                h = divmod(int(h) / CM_PER_INCH, 12) 
                h = "%d\'%d\"" % h
            elif len(h) < 3:
                h += '0"'
            else:
                h += '"'
            height = h

        weight = WEIGHT_RE.search(r.text)
        if weight:
            i = weight.lastindex
            if i > 1:
                conversion = 2.20462
            else:
                conversion = 1
            weight = int(int(weight.group(i)) * conversion)
            
        res = RESULTS_RE.search(r.text)
        score, mods = None, None
        if res:
            res, mods = res.group(1), res.group(2)
            if ":" in res and res.split(":")[1]:
                m, s = res.split(":")
                score = int(m) * 60 + int(s)
            else:
                score = int(re.sub("[^0-9]", "", res)) * 60

        units = UNITS_RE.findall(str(r.workout))
        if units:
            units = units[0]
        else:
            units = None
        
        result = Result(workout_id = r.workout_id,
                        comment_id = r.id,
                        user_id = r.user_id,
                        gender = gender,
                        age = age,
                        height = height,
                        weight = weight,
                        result = res,
                        score = score,
                        units = units,
                        mods = mods)

        results.append(result)
    return results

def add_results_to_db(results, session):
    session.bulk_save_objects(results)

def get_workout_min_max_avg(workout):
    # initialize variables with first non-None type score

    if workout.results:
        
        initialized = False
        i, total = 0, 0

        for result in workout.results:
            if result.score is not None:
                rMin = rMax = result.score
                initialized = True
                break

        if initialized:
            for result in workout.results:
                if result.score:
                    i += 1
                    total += result.score
                    if result.score < rMin:
                        rMin = result.score
                    elif result.score > rMax:
                        rMax = result.score

            return (rMin, rMax, total / i)
        else:
            return (None, None, None)

def get_results_min_max_avg(results):
    # initialize variables with first non-None type score 
    initialized = False
    i, total = 0, 0

    for result in results:
        if result.score is not None:
            rMin = rMax = result.score
            initialized = True
            break

    if initialized:
        for result in results:
            if result.score:
                i += 1
                total += result.score
                if result.score < rMin:
                    rMin = result.score
                elif result.score > rMax:
                    rMax = result.score

        return (rMin, rMax, total / i)
    else:
        return (None, None, None)

# sess = setup_session()
# rr, r = scrub(sess)
# add_results_to_db(r, sess)
# for i in r[0:100]:
#     print (i.comment_id, i.gender, i.age, i.height, i.weight, i.result)
# fran = sess.query(Result).filter(Result.workout_id==209, Result.mods.like("%rx%"))
# get_results_min_max_avg(fran.all())
