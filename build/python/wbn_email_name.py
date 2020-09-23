# general
import os
import random
import csv

# wolfram alpha
import wolframalpha

# images
import urllib.request

# email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# secrets
import secrets

# constants

gbl_str_path_output = "/python/output/" # end with last /

# randomize
gbl_str_gender = random.choice(['boys','girls'])
gbl_int_rank = random.randint(1,5000)

# wolfram alpha client
wc = wolframalpha.Client(secrets.gbl_str_app_id)
question = " ".join(["#" + str(gbl_int_rank), gbl_str_gender, "name"]) # ie "#1 boys name"
print(question)
res = wc.query(question)

# save raw data

dict_raw = {}
int_pod = 0

for pod in res.pods:
    
    dict_raw[int_pod] = {}
    
    sub = next(pod.subpods) # there's only one
    if sub['plaintext'] is not None:
        dict_raw[int_pod] = sub['plaintext'].split('\n')
    else:
        dict_raw[int_pod] = {'@src': sub['img']['@src'], '@alt': sub['img']['@alt']}
    
    int_pod = int_pod + 1

# downlaod images

str_path_img_history = os.path.join(gbl_str_path_output, gbl_str_gender + " " + str(gbl_int_rank).zfill(5) + " " + dict_raw[1][0] + "-history.jpg")
str_path_img_age = os.path.join(gbl_str_path_output, gbl_str_gender + " " + str(gbl_int_rank).zfill(5) + " " + dict_raw[1][0] + "-age.jpg")

urllib.request.urlretrieve(dict_raw[3]['@src'], str_path_img_history)
urllib.request.urlretrieve(dict_raw[5]['@src'], str_path_img_age)

# send email
# https://realpython.com/python-send-email/

sender_email = secrets.gbl_str_un

# get receiver email from CSV
# receiver_email = ["john_doe@gmail.com"]
with open('/python/input/emails.csv', newline='') as f:
    reader = csv.reader(f)
    receiver_email = [row[0] for row in reader]

message = MIMEMultipart("alternative")
message["Subject"] = "Baby Name: " + dict_raw[1][0]
message["From"] = sender_email
message["To"] = ", ".join(receiver_email)

if 8 in dict_raw.keys():
    str_meaning = dict_raw[8][0]
else:
    str_meaning = "[no meaning found]"

text = """
""" + dict_raw[1][0] + """
""" + str_meaning

# improvement: need error handling (eg meaning)
html = """\
<html>
  <head></head>
  <body>
    <h1>""" + dict_raw[1][0] + """</h1>
    <b style='color:blue'><i>""" + str_meaning + """</i></b>

    <h2>Random Stats</h2>
    <ul>
        <li>""" + dict_raw[2][0].split("|")[1].strip() + """ most popular</li>
        <li>""" + dict_raw[2][1].split("|")[1].strip() + """</li>
        <li>""" + dict_raw[2][2].split("|")[1].strip() + """</li>
        <li>""" + dict_raw[4][0].replace("|","=") + """</li>
        <li>""" + dict_raw[4][3].replace("|","=") + """</li>
    </ul>
    
    <h2>""" + dict_raw[3]['@alt'] + """</h2>
    <img src="cid:image1">
    
    <h2>""" + dict_raw[5]['@alt'] + """</h2>
    <img src="cid:image2">"""
    
if 7 in dict_raw.keys():
    html = html + """\
        <h2>Famous Examples</h2>
        <ul>
        """ + "\n".join(["<li>" + str_example + "</li>" for str_example in dict_raw[7]]) + """
        </ul>
        """
    
    html = html + """\
    <h2>Sources</h2>
    <ul>
        <li>""" + dict_raw[2][3][1:-1] + """</li>
        <li>""" + dict_raw[4][4][1:-1] + """</li>
    </ul>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
message.attach(part1)
message.attach(part2)

# download, encode, and attach image

fp = open(str_path_img_history, 'rb')
msgImage_history = MIMEImage(fp.read())
fp.close()

fp = open(str_path_img_age, 'rb')
msgImage_age = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above

msgImage_history.add_header('Content-ID', '<image1>')
message.attach(msgImage_history)

msgImage_age.add_header('Content-ID', '<image2>')
message.attach(msgImage_age)

# connect to gmail
# for this to work, we need to turn ON less secure app access

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, secrets.gbl_str_pw)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )