#!/usr/bin/env python3
# ==========================================================
# Copyright 2020 519Seven
# ==========================================================
''' Designed for cron - scp files to web server '''
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

# Logging to syslog
#handler = logging.handlers.SysLogHandler(address='/var/run/syslog', facility=syslog.LOG_LOCAL1)
#handler.ident = 'needed_for_macos'
#my_logger = logging.getLogger('scpLogger')
#my_logger.setLevel(logging.DEBUG)
#my_logger.addHandler(handler)
# Logging to a file
#logging.basicConfig(filename='scptoweb.log', level=logging.DEBUG)
#logging.debug('Logging to file?')
#logging.info('Info to file?')
#logging.warning('Warning to file?')

# This works on macos
syslog.openlog("scptoweb")

def scp_files(ws, pt, fd, su, pk, kh):
    ''' Using SCPClient, loop through directory and scp files to remote dir'''

    syslog.syslog(syslog.LOG_ALERT, "Starting scptoweb ...")
    rsakey = RSAKey.from_private_key_file("/Users/peter.akey/.ssh/ithelper_pakey-imac_id")
    ssh = SSHClient()
    ssh.load_system_host_keys(filename=kh)
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        #my_logger.info('Connecting to {0}...'.format(ws))
        syslog.syslog(syslog.LOG_ALERT, "Connecting to {0} ...".format(ws))
        ssh.connect(ws, port=pt, username=su, pkey=rsakey, auth_timeout=22)
    except TimeoutError as testr:
        syslog.syslog(syslog.LOG_ALERT, "{0}: {1}".format(ws, testr))
        sys.exit(2)
    except SSHException as sshe:
        syslog.syslog(syslog.LOG_ALERT, "{0}: {1}".format(ws, sshe))
        sys.exit(3)

    with SCPClient(ssh.get_transport()) as scp:
        #my_logger.info('Scanning {0}...'.format(fd))
        syslog.syslog(syslog.LOG_ALERT, "Scanning {0} ...".format(fd))
        for entry in os.scandir(fd):
            filename = entry.name
            filepath = entry.path
            try:
                if filename.endswith(".pdf") or filename.endswith(".doc") or filename.endswith(".docx"):
                    syslog.syslog(syslog.LOG_ALERT, "Uploading {0} ...".format(fd))
                    scp.put(filepath, remote_path='Site_Files')
            except FileNotFoundError as fnfe:
                #my_logger.info('{0}: {1}'.format(fd,fnfe))
                syslog.syslog(syslog.LOG_ALERT, "{0}: {1}".format(fd,fnfe))
        scp.close()
    return 0


if __name__ == '__main__':
    ''' SCP to remote webserver, details are pulled from environment'''

    i = 5
    for param in ['WEBSERVER', 'PORT', 'FILESDIR', 'SCPUSER', 'PKEY', 'KNOWNHOSTS']:
        try:
            os.environ[param]
        except KeyError:
            print("{0} env var must be set prior to calling this script".format(param))
            sys.exit(i)
        i += 1
    WEBSERVER = os.environ['WEBSERVER']
    PORT = os.environ['PORT']
    FILESDIR = os.environ['FILESDIR']
    SCPUSER = os.environ['SCPUSER']
    PKEY = os.environ['PKEY']
    KNOWNHOSTS = os.environ['KNOWNHOSTS']

    sys.exit(scp_files(WEBSERVER, PORT, FILESDIR, SCPUSER, PKEY, KNOWNHOSTS))
