# coding=utf-8
from __future__ import absolute_import

import json
import logging
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText
from email.header import Header


class MailSender(object):
    """ MailSender used to send mail"""

    @staticmethod
    def __contains_nonascii_characters(string):
        """ check if the body contain nonascii characters"""
        for c in string:
            if not ord(c) < 128:
                return True
        return False

    def __addheader(self, msg, headername, headervalue):
        """ judge the message's charset and set header with "utf-8"
            when there is nonascii characters
        """
        if self.__contains_nonascii_characters(headervalue):
            h = Header(headervalue, 'utf-8')
            msg[headername] = h
        else:
            msg[headername] = headervalue
        return msg

    def __init__(self, smtp_server, smtp_user, smtp_password,
                 smtp_port=25, is_with_tls=False):

        """
        Initial with smtp_user and password

        Parameters
        ----------
        smtp_host: string
            smtp host ip address
        smtp_user : string
            smtp user name
        smtp_password : string
            smtp password

        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.is_with_tls = is_with_tls

    def send(self, mail_from, mail_to_list,
             mail_subject, mail_body, mime_type="html"):
        """
        send mail to dest recipients

        Parameters
        ----------
        mail_from : string
            sender's mail address
        mail_to_list : array
            recipient's mail addresses

        """
        if not isinstance(mail_to_list, list):
            logging.error("no mail to list.")
            return

        msg = MIMEMultipart()
        if isinstance(mail_body, unicode):
            mail_body = mail_body.encode('utf-8')
        plaintext = MIMEText(mail_body, mime_type, 'utf-8')

        msg.attach(plaintext)
        msg["From"] = mail_from
        msg['BCC'] = ', '.join(mail_to_list)
        if len(mail_to_list) is 1:
            msg['To'] = msg['BCC']

        msg["Subject"] = mail_subject
        msg['Date'] = formatdate(localtime=True)

        # login to smtp server
        if self.smtp_server is None:
            logging.error("no smtp server provided.")
            return
        if self.smtp_user is None:
            logging.error("no smtp user provided.")
            return
        if self.smtp_password is None:
            logging.error("no smtp password provider.")
            return
        try:
            if self.is_with_tls:
                server = smtplib.SMTP(self.smtp_server)
                server.starttls()
            else:
                server = smtplib.SMTP(self.smtp_server)
            server.login(self.smtp_user, self.smtp_password)    # optional
            server.sendmail(msg['from'], mail_to_list, msg.as_string())
            server.close()
        except Exception as e:
            logging.error("send mail error %r" % (e,))


class MailQueueWatcher(object):
    rds_queue_key = "mail_queue"
    mail_from = "nobody"

    def __init__(self, rds_conn):
        self.rds_conn = rds_conn
        return

    def watch(self):
        print "-------------------------"
        print "Mail Queue Watcher: Start"

        while True:
            queue_name, mail_data = self.rds_conn.brpop(self.rds_queue_key, 0)
            # print "get mail: %s" % (mail_data,)

            try:
                mail = json.loads(mail_data)
                mail_from = mail["from"] or self.mail_from
                mail_to = mail["to"]
                mail_subject = mail["subject"]
                mail_body = mail["body"]
                smtp = mail["smtp"]
                smtp_server = smtp["server"]
                smtp_user = smtp["user"]
                smtp_password = smtp["password"]
            except Exception as e:
                logging.error("parse mail error %r" % (e,))
                continue
            try:
                self.mailer = MailSender(smtp_server,
                                         smtp_user,
                                         smtp_password)

                self.mailer.send(mail_from,
                                 mail_to,
                                 mail_subject,
                                 mail_body)
            except Exception as e:
                logging.error("Sending Error %r " % (e,))

            time.sleep(5)
