import re

"""
Identifies gender, age, height, weight, and completion time
in comment.
"""

# Examples:
# male
# aweofijbie
# male eating tamales
# female
# MALE
# aweofij
# FEmale eating TAMALES
# M40yr 5'10" 174LB
# Nathan Smetzer BW: 245 (up 5lbs...) \nHeight: 66" (5'6")
# Male, 55, 5'10", 177 LBS
# M/40/145 pounds/5'6"
# M/29/180cm/80kg
# 53/5'8"/155
# M. 55. 178 LBS.
# 47yo/M/5'8"/185ish
# 40 yr old male / 5'9 / 206 lbs
# 47yo/M/5'8"/185ish
# 33/M/175#/6'
# M / 28 / 5'10 / 230#


# Both expressions below are functionally identical

# GENDER_RE = re.compile(r'female|(?<![a-zA-Z])male|(?<![a-zA-Z])[mf](?![a-zA-Z])(?i)')

GENDER_RE = re.compile(r"""female|            # self explanatory
                           (?<![a-zA-Z])male| # prevents false matches like spam
                           (?<![a-zA-Z])      # same negative lookbehind assertion
                           [mf]               # so that /M/ or /F/ are acceptable
                           (?![a-zA-Z])       # negative lookahead assertion
                           (?ix)""")          # ignore case and allow verbose cmts


# AGE_RE = re.compile(r"(?<![\d'\"])[1-7][0-9](?![\d#'\"]|kg|lb)")

AGE_RE = re.compile(r"""(?<![\d'\"]) # prevent matches of digits, single or double quotes b4
                        [1-7][0-9]   # the main part, which reqs two digits 10-79 and
                        (?![\d#'\"]| # prevent matches of digits, #, single, double quotes,
                        kg|lb)       # kg, or lb after main part
                        (?ix)""")    # ignore case and allow verbose cmts

# HEIGHT_RE = re.compile(r"\d\s?'\s?\d{0,2}\"?")

HEIGHT_RE = re.compile(r"""\d            # feet
                           \s?           # allow for 0 or 1 space
                           '             # confirm it is in feet
                           \s?           # allow for 0 or 1 space
                           \d{0,2}       # inches can be nothing, 1 or 2 digits 
                           \"?           # inches quote is optional         
                           (?x)""")

# BODYWEIGHT_RE = re.compile(r"(?<![\d'\"])[1-3]\d{2}(?![\d'\"]|m|cm|ft|in|yr|yo|year)")

BODYWEIGHT_RE = re.compile(r"""(?<![\d'\"]) # prevent matches of digits, single or double quotes b4 
                               [1-3]\d{2}   # the main part, which reqs 3 digits 100-399 and
                               (?![\d'\"]   # prevent matches of digits, single, double quotes,
                               |m|cm|ft|in  # height,
                               |yr|yo|year) # or age after main part
                               (?ix)""")    # ignore case and allow verbose cmts

def valid_gender(comment):
    return comment and GENDER_RE.match(comment)

