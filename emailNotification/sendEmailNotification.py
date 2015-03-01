# Sends an email notification to user specified in arguments
# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Zaynab Alattar
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def sendEmailNotification(userName, userEmail):
	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open('message.txt', 'rb')
	# Create a text/plain message
	msg = MIMEText(fp.read())
	fp.close()

	# From == the sender's email address 
	# To == the recipient's email address
	msg['Subject'] = 'Notification of Query Result'
	msg['From'] = 'BPA'												# CHANGE ME
	msg['To'] = str(userName)

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	server = smtplib.SMTP('smtp.gmail.com', 587)
	# server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.login('bpa.psucapstone@gmail.com', 'NicolaTesa')
	server.sendmail('bpa.psucapstone@gmail.com', str(userEmail), str(msg))
