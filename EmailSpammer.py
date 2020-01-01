#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import json
import smtplib
from email.message import EmailMessage

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Email spammer')
   parser.add_argument('meta', action='store', type=str,
      help='The json file containing the email metadata.')
   parser.add_argument('recipients', action='store', type=str,
      help='The text file containing the recipients.')
   parser.add_argument('email', action='store', type=str,
      help='The file containing the email in HTML form.')

class EmailSpammer:
   def __init__(self):
      self.recipients = set()
      self.subject = ''
      self.emailHtml = ''
      self.gmailUsername = ''
      self.gmailPassword = ''
   def setMetaData(self, metaData: dict):
      if 'Subject' in metaData:
         self.subject = metaData['Subject']
      else:
         print("Error: Missing subject from metadata")
         sys.exit(1)
      if 'Gmail' in metaData:
         if 'Username' in metaData['Gmail']:
            self.gmailUsername = metaData['Gmail']['Username']
         if 'Password' in metaData['Gmail']:
            self.gmailPassword = metaData['Gmail']['Password']
      else:
         print("Error: Missing Gmail data from metadata")
         sys.exit(1)
   def setRecipients(self, recipients: list):
      self.recipients.update(recipients)
   def setSender(self, sender: str):
      self.sender = sender
   def setEmailHtml(self, email: str):
      self.emailHtml = email
   def sendEmail(self):
      #Gmail sign in
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.login(self.gmailUsername, self.gmailPassword)
      #Send emails individually
      for recipient in self.recipients:
         emailMessage = EmailMessage()
         emailMessage['Subject'] = self.subject
         emailMessage['From'] = self.gmailUsername
         emailMessage['To'] = recipient
         emailMessage.set_content(self.emailHtml)
         emailMessage.add_alternative(self.emailHtml, subtype='html')
         server.send_message(emailMessage)
      server.quit()

if __name__ == '__main__':
   args = parser.parse_args()

   emailSpammer = EmailSpammer()
   with open(args.meta, 'r', encoding='iso-8859-1') as metaFile:
      emailSpammer.setMetaData(json.load(metaFile))
   with open(args.recipients, 'r', encoding='iso-8859-1') as recipientsFile:
      recipients = list()
      for line in recipientsFile.readlines():
         line = line.replace('\r','').replace('\n','')
         recipients.append(line)
      emailSpammer.setRecipients(recipients)
   with open(args.email, 'r', encoding='iso-8859-1') as emailFile:
      if emailFile.name.endswith('.html'):
         emailSpammer.setEmailHtml(emailFile.read())
         emailSpammer.sendEmail()
      else:
         print("Error: Email file not an html file")
         sys.exit(1)
   sys.exit(0)
