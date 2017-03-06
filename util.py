import re

"""
Identifies gender, age, height, weight, and completion time
in comment.
"""

# Gender returns (before, gender, after).
# M = male, F = female
# combine before and after, then pass into remaining regex
# GENDER_RE = re.compile(r"""^(.*)([mf])\/(.*)$(?im)""")

GENDER_RE = re.compile(r"""
                          ^(?:.*?)                 # capture anything before the main bit
                          ([mf](?=\s?\/)|
                          male|female)             # strict lookup. high hit rate
                          (?imx)
                       """)

# GENDER_RE = re.compile(r"""([mf])\/(?i)""")    # strict lookup. high hit rate.

# Age returns age
AGE_RE = re.compile(r"\/([1-9][0-9])\/")   # strict lookup. high enough hit rate.

# Height returns (feet, inches, all_inches, cm).
# Expected results are
# (feet, inches, None,   None)
# (None, None,   inches, None)
# (None, None,   None,   cm)
# HEIGHT_RE = re.compile(r"""([3-7])\'(\d{0,2})|([3-9][0-9])\"|(\d{2,3})\s?cm(?i)""")

HEIGHT_RE = re.compile(r"""
                            ([3-7])\'(\d{0,2})  # normal feet and inches, inches optional
                            |
                            ([3-9][0-9])\"      # or all inches. Assumes 3ft to 7ft
                            |
                            (\d{2,3})\s?cm      # or all cms.
                            (?ix)
                        """)

# Weight matches returns (lbs, kg).
# Expected results are
# (lbs, None)
# (None, kgs)
# WEIGHT_RE = re.compile(r'\/([1-3][0-9][0-9])(?!c)|\/(\d{2,3})\s?kg(?i)')

WEIGHT_RE = re.compile(r"""
                            \/                  # must start with slash
                            ([1-3][0-9][0-9])   # min 100 lbs
                            (?!c)               # make sure not height measure
                            |
                            \/(\d{2,3})\s?kg    # or 2-3 digit weight in kg
                            (?ix)
                        """)

# Unit match returns the measure for results
# e.g. time, round, reps, load, etc.
UNITS_RE = re.compile(r"post.*(time|round|rep|load|total|calorie)(?i)")  

# Results match returns the time/rep/points
# e.g. 4:30, 350#, 150 reps\
RESULTS_RE = re.compile(r'^(?:.*?)(\d+:\d+)\s?(rx|min)(?im)')
