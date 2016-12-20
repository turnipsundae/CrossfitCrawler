from database_setup import Base, Workout, Comment, User, engine
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getWorkoutAndComments(abs_url, browser):

  # initialize outputs
  title = ""
  description = ""
  comments = []

  # open the page
  browser.get(abs_url)
  print ("Getting url...")
  
  # get the meta tags, which hold the WOD title and description
  metatags = browser.find_elements_by_xpath('/html/head/meta')
  for meta in metatags:
    if meta.get_attribute('property') == 'og:title':
      title = meta.get_attribute('content')
    if meta.get_attribute('property') == 'og:description':
      description = meta.get_attribute('content')

  # get the comments container
  commentsContainer = browser.find_element_by_id('commentsContainer')

  # get the comments
  commentPartial = commentsContainer.find_elements_by_class_name('comment-partial')

  # and extract the name and text for each comment (no children)
  for comment in commentPartial:
    name = comment.find_element_by_class_name('name').text
    text = comment.find_element_by_class_name('text').text
    comments.append((name, text))

  return (title, description, comments)

def crawl(engine, initial_url, start_date, end_date, delay=1):
  """
  Get the title and description of each workout of the day
  between start and end date. Initializes with a seed url.
  """

  # create a session to hook up with the sqlite db
  Session = sessionmaker(bind=engine)
  session = Session()

  # get the date range
  date_range = end_date - start_date
  
  # make a list of dates
  dates = [start_date + timedelta(date) for date in range(0, date_range.days)]

  # initialize a web browser
  browser = webdriver.Firefox()

  # ensure we wait for DOM to populate
  browser.implicitly_wait(10)

  # The url for workouts of the days are formatted as
  # https://www.crossfit.com/workouts/2016/01/15
  # where the last three parameters are year, month, day.
  for date in dates:
    
    # build the url
    abs_url = initial_url + "/{:02d}/{:02d}/{:02d}".format(date.year, date.month, date.day)
    
    # get the contents
    title, description, comments = getWorkoutAndComments(abs_url, browser)

    # and write them to the db
    w = Workout(title=title, description=description)
    session.add(w)
    session.commit()
    print ("Added {} to the DB.".format(title))

    for (username, text) in comments:
      u = User(username=username)
      session.add(u)
      session.commit()

      c = Comment(text=text, user_id=u.id, workout_id=w.id)
      session.add(c)
      session.commit()

    print("Added {} user comments to the DB.".format(session.query(Comment).count()))
    # delay between requests
    # time.sleep(delay)

  return session

crossfit = "https://www.crossfit.com/workout"
start_date = datetime(2016, 1, 3)
end_date = datetime(2016, 11, 30)

session = crawl(engine, crossfit, start_date, end_date)
