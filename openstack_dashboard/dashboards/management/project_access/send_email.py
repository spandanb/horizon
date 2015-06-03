import smtplib
from django.conf import settings
from openstack_dashboard.api import keystone

def send_email(msg_type, msg_dict):
    """
    Sends email to admin from no_reply.
    Creates message based msg_type and key-value pairs
    specificied in msg_dict
    """

    user_email = keystone.get_user_email(msg_dict["user_id"])

    FROM = settings.EMAIL_HOST_USER
    TO = [settings.ADMIN_EMAIL, user_email] 
    
    if msg_type == "new":
        SUBJECT = "[HORIZON] Request to Create New Project "
        TEXT = ("Hello admin, \n{0[username]} ({0[user_id]}) "
                "requested to create a project called {0[project]}. "
                "The purpose of the project is to: {0[description]}. "
                "The user is affiliated with {0[institution]}. The principal "
                "in this project is {0[principal]}.").format(msg_dict)
    
    elif msg_type == "leave":
        SUBJECT= "[HORIZON] Request to Leave Project"
        TEXT = ("Hello admin, \n{0[username]} ({0[user_id]}) "
                "requested to leave project "
                "{0[project]} ({0[project_id]}.").format(msg_dict)

    elif msg_type == "join":
        SUBJECT = "[HORIZON] Request to Join Project"
        TEXT = ("Hello admin, \n{0[username]} ({0[user_id]}) "
                "requested to join project "
                " {0[project]} ({0[project_id]}).").format(msg_dict)

    # Prepare email 
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) 
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        pass
