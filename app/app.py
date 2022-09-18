import flask
import re
import os
import hashlib
from app.mail import Mail
mailReminder = flask.Flask(__name__)

# url /remind?addr=xx@xx&subject=xx&message=xx&token=xx
# return {
#    "success": true|false,
#    "message": "success"|"error message"
# }
@mailReminder.route('/remind')
def remind():
    ref_md5 = os.environ.get("REF_MD5")
    if ref_md5 is None:
        return {
            "success": False,
            "message": "Please provide the md5 of the reference string in environment variable REF_MD5"
        }
    # get md5 of the token
    token = flask.request.args.get("token")
    if token is None:
        return {
            "success": False,
            "message": "Please provide the token"
        }
    token_md5 = hashlib.md5(token.encode()).hexdigest()
    if token_md5 != ref_md5:
        return {
            "success": False,
            "message": "Invalid token"
        }

    addr = flask.request.args.get('addr')
    # check whether the addr is valid
    regex = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if not re.match(regex, addr):
        return {
            "success": False,
            "message": "Invalid email address"
        }, 400
    subject = flask.request.args.get('subject')
    # subject cannot be empty
    if subject == "":
        return {
            "success": False,
            "message": "Subject cannot be empty"
        }, 400
    message = flask.request.args.get('message')
    try:
        m = Mail()
        m.send_mail(addr,subject,message)
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }, 500
    return {
        "success": True,
        "message": "success"
    }
    