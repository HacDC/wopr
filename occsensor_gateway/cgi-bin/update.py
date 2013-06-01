#!/usr/bin/env python

import cgi
import time
import os
import sys
import cgitb ;cgitb.enable()

'''
message format:
	subject: Lights=$lightsOn
	body: GPIO4=$GPIO4;GPIO5=$GPIO5;FA3=$FA3;FA4=$FA4;FA5=$FA5
	date: $( echo $(date "+%A, %b %d at %l:%M %p") | tr ' ' '_') aka %A,_%b_%d_at_%l:%M_%p and TZ='EST5EDT,M3.2.0,M11.1.0'
'''
DATE_FORMAT='%A, %b %d at %I:%M %p' # %l == %I
BODY_FIELD_SEP=';'
BODY_KEY_VAL_SEP='='
BODY_KEYS=('GPIO4', 'GPIO5', 'FA3', 'FA4', 'FA5')

def set_GMT():
	os.environ['TZ'] = 'GMT'
	time.tzset()

def set_EDT():
	os.environ['TZ'] = 'US/Eastern'
	time.tzset()

class Sensor:
	def __init__(self, id, label, boolean={True:'on', 'true':'on', False:'off', 'false':'off'}):
		self.id = id
		self.label = label
		self.boolean = boolean

sensor_info = {'Lights':Sensor('Lights', 'one or more lights'), 'FA3':Sensor('FA3', 'hall light'), 'FA4':Sensor('FA4', 'main room light'), 'FA5':Sensor('FA5','work room light')}


class Errors:
	def __init__(self):
		self.errlist = []
	
	def add(self, error='', exception=None):
		if exception:
			error += str(repr(exception))
		self.errlist.append(error)
	
	def to_string(self):
		return '\n'.join(self.errlist)

errors = Errors()

class DefaultField:
	def __init__(self, name, default=None, ftype=str, required=True):
		self.name = name
		self.default = default
		self.ftype = ftype
		self.required = required
		self._value = self.ftype(default)

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, new_val):
		if type(val) == self.ftype:
			self._value = new_val
		else:
			try:
				self._value = self.ftype(new_val)
			except TypeError as e:
				errors.add(exception=e)

fileds = [DefaultField('subject'), DefaultField('date'), DefaultField('body',default=[],ftype=list)]

def collect_new_values(reqs):
	reqs_dict = {}
	for field in fileds:
		if field.ftype == list:
			value = reqs.getlist(field.name)
		else:
			value = reqs.getfirst(field.name)
		if field.required and not value:
			errors.add('Missing field "%s". Found value: %s' % (field.name,value))
		errors.add(str((field.name, value)))
		reqs_dict[field.name] = value
	return reqs_dict

def valid_date(date_str, fmt=DATE_FORMAT):
	date_str = date_str.replace('_', ' ')
	try:
		return time.strptime(date_str, fmt)
	except Exception as e:
		errors.add(str(repr(e)))
		return None

def valid_subject(string):
	sub = string.split('=', 1)
	if len(sub) != 2: return None
	if sub[0].lower() != 'lights': return None
	if sub[1].lower() not in ('true', 'false'): return None
	return {'Lights':bool(sub[1])}

def valid_body_field(string):
	sub = string.split(BODY_KEY_VAL_SEP, 1)
	if len(sub) != 2: return None
	if sub[0] not in BODY_KEYS: return None
	if sub[1].lower() not in ('true', 'false'): return None
	return {sub[0]:sub[1]}

def valid_body(body):
	if len(body) < 1: return None
	body_dict = {}
	for s in body:
		errors.add(s)
		d = valid_body_field(s)
		if d:
			body_dict.update(d)
	if body_dict: return body_dict
	return None

def sensor_vals2str(sensor_vals):
	s = []
	for k,v in sensor_vals.items():
		s.append('%s is %s' % (sensor_info[k].label, sensor_info[k].boolean[v]))
	return ', '.join(s)

def format_message(date, sensor_vals):
	d = {'default':'HacDC is %s since %s' % ({True:'open', False:'closed'}[sensor_vals['Lights']], time.strftime('%I:%M%p %A %d %b', date)),
		'human': sensor_vals2str(sensor_vals),
		'raw':str(sensor_vals)}
	return d

def handle_request(reqs):
	reqs_dict = collect_new_values(reqs)
	if not reqs_dict: return errors.to_string('failed to collect values from parameters')
	date = valid_date(reqs_dict['date'])
	if not date: errors.add('Invalid date format: %s' % reqs_dict['date'])
	subject = valid_subject(reqs_dict['subject'])
	if not subject: errors.add('Invalid subject field: %s' % reqs_dict['subject'])
	body = valid_body(reqs_dict['body'])
	if not body: errors.add('Invalid body field: %s' % reqs_dict['body'])
	if date and subject and body:
		subject.update(body)
		sensor_vals = subject
		return format_message(date, sensor_vals)
	return errors.to_string()
	

def main(args=[]):
	print('Content-Type: text/html\n\n')
	print('SOM<br/>')
	msg = handle_request(cgi.FieldStorage())
	print(msg)
	print('<p>ERRORS</p>'+errors.to_string())
	print('<br/>EOM')

main()
