from bottle import Bottle, run, route, static_file, request, response, template, redirect
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from string import Template
import json
import pymongo
import requests
import datetime
import time
import math
import hashlib as hl
import os
import smtplib
import boto3
import uuid

app = Bottle(__name__)

# client = MongoClient('')
# db = client.db_name

# Start of s3 upload section

@app.get('/')
def root():
	return "Hello!!!"


@app.get('/hello/<name>')
def hello(name):
	return "Hi " + name + "!!"

@app.get('/web')
def web():
	return static_file('index.html', root='./')

@app.route('/sign_s3')
def sign_s3():
	S3_BUCKET = 'sw-test-123'

	file_name = request.GET.get('file_name') + '-' + uuid.uuid4().hex
	file_type = request.GET.get('file_type')

	s3 = boto3.client('s3')

	presigned_post = s3.generate_presigned_post(
		Bucket = S3_BUCKET,
		Key = file_name,
		Fields = {"acl": "public-read", "Content-Type": file_type},
		Conditions = [
		  {"acl": "public-read"},
		  {"Content-Type": file_type}
		],
		ExpiresIn = 3600
	)

	return json.dumps({
	'data': presigned_post,
	'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
	})

@app.get('/s3_test')
def s3_test():
	return static_file('s3_test.html', root='./')

@app.get('/sendEmail')
def sendEmail():

	email_id = request.GET.get('email')
	email_sub = request.GET.get('sub')
	email_msg = request.GET.get('msg')

	header  = 'From: Sertify<suraj@sertify.me>\n'
	header += 'To: ' + email_id + '\n'
	header += 'Subject: ' + email_sub + '\n\n'

	message = email_msg

	message = header + message

	server = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
	server.starttls()
	server.login('','')
	
	problems = server.sendmail('suraj@sertify.me', email_id, message)
	
	server.quit()

	return {'status': 'ok', 'data': 'email sent'}