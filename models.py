__author__ = 'mike.davis'

from google.appengine.ext import db
from google.appengine.ext import blobstore

class Submission(db.Model):
    name = db.StringProperty()
    time = db.DateTimeProperty(auto_now_add=True)
    email = db.StringProperty()
    uid = db.StringProperty()

class Fall2013ISUCDC(db.Model):
    name = db.StringProperty()
    time = db.DateTimeProperty(auto_now_add=True)
    email = db.StringProperty()
    uid = db.StringProperty()
