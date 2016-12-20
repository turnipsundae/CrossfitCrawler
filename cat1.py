import re

"""
Identifies gender, age, height, weight, and completion time
in comment.
"""

DEMO_RE = re.compile(r"(((^)|(\s))[MmFf][^a-zA-Z](\d+[^a-zA-Z]*)+$")
# (^) | (\s)      matches a new line OR a unicode white space
# [MmFf][^a-zA-Z] followed by the gender, no trailing characters
# \d+             match any unicode decimal digit, one or more of them
# [^a-zA-Z]*      ensure there aren't letters following the digit(s)
# +$              ensure there is one or more of those patterns
#                 and they don't spill over to the next line
#                 use this tool to help deconstruct: http://regexr.com/

# Examples of known-misses:
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


# Examples of known-errors:
# 19 : 40

GENDER_RE = re.compile(r'^(fe)*male(?!\w)|[^\w](fe)*male(?i)')
GENDER_RE = re.compile(r'[mf](?![a-zA-Z])(?im)') # will capture words like BAM
GENDER_RE = re.compile(r'^[mf](?![a-zA-Z])(?im)|[^a-zA-Z\'][mf](?![a-zA-Z])(?im)')
GENDER_RE = re.compile(r'((female|male|^[mf](?![a-zA-Z])|[^a-zA-Z\'][mf](?![a-zA-Z]))(?im))')
GENDER_RE = re.compile(r'((female|male|(^[mf](?![a-zA-Z]))|([^a-zA-Z\'][mf](?![a-zA-Z])))(?im))')



GENDER_RE = re.compile(r'male')

GENDER_RE = re.compile(r'(male)(?im)|(female)(?im)|^[mf](?![a-zA-Z])|[^a-zA-Z\'][mf](?![a-zA-Z])(?im)')


def valid_gender(comment):
    return comment and GENDER_RE.match(comment)

