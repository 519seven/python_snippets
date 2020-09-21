#!/usr/bin/env python3
# ==========================================================
# Copyright 2020 519Seven
# ==========================================================
''' Designed for cron - scp files to web server 
	Set up SSH key for password-less SCP to web server
	Using env vars because this in a place where 
	curious minds want to know 						     '''
# Upload files that match criteria to remote web server
# If the file has an extension that falls into the list
#   upload it to our web server. A cronjob on the web
#   server will examine the filename and copy it to the
#   appropriate location on the web server.
# PREREQUISITES:
#   envvars: WEBSERVER - the URL of the target for scp
#            FILESDIR  - the directory for copying files to
#   python3 -m pip install scp
#   python3 -m pip install paramiko
# OUTCOME:
#   files are copied and removed if successfully copied
# ==========================================================

from paramiko import RSAKey
from paramiko import SSHClient
from paramiko import SSHException
from paramiko import AutoAddPolicy
from scp import SCPClient    # https://pypi.org/project/scp/
import logging
import logging.handlers
import os
import sys
import syslog
import json, os
import shlex
import subprocess as subp

syslog.openlog("scptoweb")

def check_env_vars():
	i = 5
	for param in ['WEBSERVER', 'PORT', 'FILESDIR', 'SCPUSER', 'PKEY', 'KNOWNHOSTS']:
		try:
			os.environ[param]
		except KeyError:
			print("{0} env var must be set prior to calling this script".format(param))
			sys.exit(i)
		i += 1


def load_env_vars():
	source = 'source ./env_vars.sh'
	dump = '/usr/bin/env python3 -c "import os, json; print json.dumps(dict(os.environ))"'
	command = shlex.split(f"/bin/bash -c {source} && {dump}")
	proc = subp.Popen(command, stdout=subp.PIPE)
	env = json.loads(proc.stdout.read())
	os.environ = env
	print(env)


def ssh_connect():
	syslog.syslog(syslog.LOG_ALERT, "Starting scptoweb ...")
	rsakey = RSAKey.from_private_key_file(f"/Users/{SCPUSER}/.ssh/rsa_id")
	ssh = SSHClient()
	ssh.load_system_host_keys(filename=KNOWNHOSTS)
	ssh.set_missing_host_key_policy(AutoAddPolicy())
	syslog.syslog(syslog.LOG_ALERT, 'Connecting to {0} ...'.format(WEBSERVER))
	ssh.connect(WEBSERVER, port=PORT, username=SCPUSER, pkey=rsakey, auth_timeout=22)


def scan_and_upload(ssh_conn):
	with SCPClient(ssh_conn.get_transport()) as scp:
		print('Scanning {0} ...'.format(FILESDIR))
		for filename in os.scandir(FILESDIR):
			if str(filename).endswith(".pdf") or str(filename).endswith(".doc") or str(filename).endswith(".docx"):
				scp.put(filename.path, remote_path='Site_Files')
	scp.close()


## Loading the environment
def main():
	''' Load env vars, connect, scan and upload '''
	load_env_vars()
	check_env_vars()

	WEBSERVER = os.environ['WEBSERVER']
	PORT = os.environ['PORT']
	FILESDIR = os.environ['FILESDIR']
	SCPUSER = os.environ['SCPUSER']
	PKEY = os.environ['PKEY']
	KNOWNHOSTS = os.environ['KNOWNHOSTS']

	ssh_conn = ssh_connect()
	scan_and_upload(ssh_conn)


if __name__ == "__main__":
	main()