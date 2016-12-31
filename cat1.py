import re

"""
Identifies gender, age, height, weight, and completion time
in comment.
"""

# GENDER_RE = re.compile(r'female|(?<![a-z])male|(?<![a-z0-9\'\"])[mf](?![a-z])(?i)')

GENDER_RE = re.compile(r"""female|              # self explanatory
                           (?<![a-zA-Z])male|   # prevents false matches like spam
                           (?<![a-zA-Z0-9\'\"])  # same negative lookbehind assertion
                           [mf]                 # so that /M/ or /F/ are acceptable
                           (?![a-zA-Z])         # negative lookahead assertion
                           (?ix)""")            # ignore case and allow verbose cmts


# AGE_RE = re.compile(r"(?<![\d'\"])[1-7][0-9](?![\d#'\"]|kg|lb)")

# AGE_RE = re.compile(r"""(?<![\d'\":]) # prevent confusion with height, time, weight
#                         [1-7][0-9]    # the main part, which reqs two digits 10-79 and
#                         (?![\d#'\":]|  # prevent matches of digits, #, single, double quotes,
#                         kg|lb)        # kg, or lb after main part
#                         (?ix)""")     # ignore case and allow verbose cmts

# Only allow for /10/ to /79/ format
# AGE_RE = re.compile(r'(?<=\/)\s?[1-7][0-9](?=\s?\/)|[1-7][0-9](?=\s?yo|yr|year)')
AGE_RE = re.compile(r"""(?<=\/)             # look for /<age>/ with
                        \s?                 # optional space between slash and number
                        [1-7][0-9]          # look for ages 10 - 79
                        (?=\s?\/)           #
                        |                   #  
                        [1-7][0-9]          # alternatively, look for 10 - 79 followed by
                        (?=\s?yo|yr|year) # yo, yr, or year
                        (?ix)""")           # ignore case and allow verbose cmts

# HEIGHT_RE = re.compile(r"[1-7]\s?'\s?\d{0,2}\"?")

HEIGHT_RE = re.compile(r"""[1-7]         # feet
                           \s?           # allow for 0 or 1 space
                           '             # confirm it is in feet
                           \s?           # allow for 0 or 1 space
                           \d{0,2}       # inches can be nothing, 1 or 2 digits 
                           \"?           # inches quote is optional         
                           (?x)""")

# BODYWEIGHT_RE = re.compile(r"(?<![\d'\"])[1-3]\d{2}(?![\d'\"]|m|cm|ft|in|yr|yo|year)")

# BODYWEIGHT_RE = re.compile(r"""(?<![\d'\"]) # prevent matches of digits, single or double quotes b4 
#                                [1-3]\d{2}   # the main part, which reqs 3 digits 100-399 and
#                                (?![\d'\"]   # prevent matches of digits, single, double quotes,
#                                |m|cm|ft|in  # height,
#                                |yr|yo|year) # or age after main part
#                                (?ix)""")    # ignore case and allow verbose cmts

BODYWEIGHT_RE = re.compile(r"(?<=\/)\s?\d{2,3}(?=\s?kg|lb)(?ix)")

def valid_gender(comment):
    return comment and GENDER_RE.match(comment)

