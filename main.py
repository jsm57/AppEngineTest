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
import webapp2
import jinja2
import os

from google.appengine.ext import ndb


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

SN_Devices = [
    {'name':"001", 'desc':"NYC"},
    {'name':"002", 'desc':"UGA"},
    {'name':"003", 'desc':"RIVERSIDE"},
    {'name':"004", 'desc':"YALE"}]

class Sensor(ndb.Model):
    name = ndb.StringProperty()
    desc = ndb.StringProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Use Google Charts API
        
        DEFAULT_DEV = "Default Device"
        
        sensor_q = Sensor.query()
        sensors = sensor_q.fetch(100)
        
        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(device=DEFAULT_DEV,sensors=sensors))

class AddSensorHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('addsensor.html')
        self.response.write(template.render())
        
    def post(self):
        newSensor = Sensor()
        # newData = JSON.parse(self.request.get('data'))
        # newSensor.name = newData.name # may be a dictionary??
        newSensor.name = self.request.get('name')
        newSensor.desc = self.request.get('desc')
        newSensor.put()
        # Good form to send the poster to somewhere (home page?)
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add', AddSensorHandler)
], debug=True)
