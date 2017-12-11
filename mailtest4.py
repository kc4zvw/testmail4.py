#!/usr/bin/env python2
#
# $Id: mailtest4.py,v 0.33 2017/12/11 20:25:15 kc4zvw Exp kc4zvw $

import datetime
import os
import smtplib
import sys

from configparser import ConfigParser

def read_hostname():
	""" Read env variable """

	host = os.environ.get('HOSTNAME')
	print("The hostname is %s" % host)
	return host

def read_datetime():
	""" get current date and time """

	now = datetime.datetime.now()
	dt = now.strftime("%A, %B %d, %Y at %H:%M:%S %p")
	print("Today is %s." % dt)
	return dt

def send_email(subject, body_text, to_email, cc_email, bcc_email):
	""" Send an email """

	base_path = os.path.dirname(os.path.abspath(__file__))
	config_path = os.path.join(base_path, "email.ini")

	if os.path.exists(config_path):
		cfg = ConfigParser()
		cfg.read(config_path)
	else:
		print("Config not found ..... Exiting!")
		sys.exit(1)

	host = cfg.get("smtp", "server")
	from_addr = cfg.get("smtp", "from_addr")

	BODY = "\r\n".join((
		"From: %s" % from_addr,
		"To: %s" % ', '.join(to_email),
		"CC: %s" % ', '.join(cc_email),
		"BCC: %s" % ', '.join(bcc_email),
		"Subject: %s" % subject ,
		"",
		body_text
		))
	email = to_email + cc_email + bcc_email

	server = smtplib.SMTP(host)
	server.sendmail(from_addr, email, BODY)
	server.quit()

if __name__ == "__main__":
	email = ["user1@example.com"]
	cc_email = ["user2@example.net"]
	bcc_email = ["user3"]

	rundate = read_datetime()
	hostname = read_hostname()

	subject = "Test email from Python on %s" % hostname
	body_text =  "\r\n".join((
		"Testing mail system via a Python script ...",
		"",
		"This is a mailed test message ran weekly to give connectivity status.",
		"Running: %s" % ''.join(rundate),
		"Details: sending output to %s and %s" % (''.join(email), ''.join(cc_email)),
		"Have a nice day!",
		"",
		"regards,",
		"",
		"David B",
		"-- ",
		"Webmaster of %s" % ''.join(hostname)
		))

	send_email(subject, body_text, email, cc_email, bcc_email)

	print("Message sent ...")

""" End of file """
