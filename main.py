#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2

from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import models
import utils
import logging

import re
import json
import urllib2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        try:
            uid = self.request.POST.get('uid')

            if uid.startswith(';600957'):
                uid = uid[7:16]

            if re.match("^[0-9]*$", uid):

                url = 'http://www.fpm.iastate.edu/roomscheduling/student_form/ajax_getISUdata.asp?returnfield=json_string&uid=%s' % uid
                response = urllib2.urlopen(url)
                output = response.read()

            else:
                url = 'http://www.fpm.iastate.edu/roomscheduling/student_form/ajax_getISUdata.asp?returnfield=json_string&email=%s@iastate.edu' % uid
                response = urllib2.urlopen(url)
                output = response.read()

            json_output = json.loads(output[12:])
            name = json_output['name']
            email = json_output['email']

            submission = models.Fall2013ISUCDC.all().filter('email =', email).fetch(1)
            if submission:
                context = {'name' : name}
                context['refresh'] = True

                path = os.path.join(os.path.dirname(__file__), 'templates/already_submitted.html')
                self.response.out.write(template.render(path, context))

            else:

                if 'NOT FOUND' in name:
                    context={'refresh' : True}
                    path = os.path.join(os.path.dirname(__file__), 'templates/not_found.html')
                    self.response.out.write(template.render(path, context))

                else:
                    submission = models.Fall2013ISUCDC(name=name, email=email, uid=uid)
                    submission.save()

                    context = {'name' : name}
                    context['refresh'] = True

                    path = os.path.join(os.path.dirname(__file__), 'templates/thank_you.html')
                    self.response.out.write(template.render(path, context))
        except Exception, e:
            path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
            self.response.out.write(template.render(path, context))


app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
