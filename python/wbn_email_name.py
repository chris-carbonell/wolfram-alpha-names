~# general
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

# funcs

def get_dict_data(str_gender, int_rank):
    '''
    organize the wolfram data into dict

    returns:
    dict_data (dict): key = my key, value = raw vale from wolfram alpha API
    '''

    # wolfram alpha client
    wc = wolframalpha.Client(secrets.gbl_str_app_id)
    
    # question 1: #n [boys/girls] name
    question_num = " ".join(["#" + str(int_rank), str_gender, "name"])
    res_num = wc.query(question_num)

    # set up landing spots
    dict_data = {}
    int_pod = 0

    # find my target info
    # some results are missing some info

    # loop over pods
    for pod in list(res.pods):
        
        for sub in pod:

            # the graph subs have None for plaintext
            if sub['plaintext'] is not None:
                # potential text target

                ls_plaintext = sub['plaintext'].split('\n')
                ls_famous = [] # landing spot for famous examples

                for str_plaintext in ls_plaintext:

                    if str_plaintext.endswith('people per year)'): 
                        # get the name itself
                        dict_data['name'] = ls_plaintext[0] # "Chris"
                        
                        # try to get origin
                        # question 2: origin of name [name]
                        
                        question_name = "origin of name " + 
                        res_name = wc.query(question_name)

                        if res_name['@success'] == 'true':
                            dict_data['origin'] = list(res_name.pod)[1]['subpod']['plaintext']

                    elif str_plaintext.startswith('rank | '):
                        # eg "rank | 613th"
                        dict_data['rank'] = str_plaintext.split("|")[1].strip() # "613th"
                    elif str_plaintext.startswith('fraction | '):
                        # eg "fraction | 1 in 4120 people (0.024%)""
                        dict_data['fraction'] = str_plaintext.split("|")[1].strip() # "1 in 4120 people (0.024%)"
                    elif str_plaintext.startswith('number | '):
                        # eg "number | 437 people per year"
                        dict_data['number'] = str_plaintext.split("|")[1].strip() # "437 people per year"
                    elif str_plaintext.startswith('expected total number alive today | '):
                        # eg "expected total number alive today | 126812 people"
                        dict_data['alive'] = str_plaintext..replace("|","=") # "expected total number alive today = 126812 people"
                    elif str_plaintext.startswith('most common age | '):
                        # eg "most common age | 49 years"
                        dict_data['mode_age'] = str_plaintext..replace("|","=") # "most common age = 49 years"
                    elif str_plaintext.startswith('(US data based'):
                        # eg "(US data based on 2018 births and other SSA registrations in the US)"
                        dict_data['source_rank'] = str_plaintext[1:-1] # "US data based on 2018 births and other SSA registrations in the US"
                    elif str_plaintext.startswith('(US data based'):
                        # eg "(using standard US mortality data)"
                        dict_data['mortality_rank'] = str_plaintext[1:-1] # "using standard US mortality data"
                    else:
                        pass
                        
                else:
                    # potential image target

                    if sub['@title'] == 'History for US births':
                        dict_data['history'] = sub['img'] # dict = {'@src': [url],'@alt': 'Chris (male given name) | etymology'}
                    elif sub['@title'] == 'Estimated current age distribution':
                        dict_data['age'] = sub['img'] # dict = {'@src': [url],'@alt': 'Estimated current age distribution'}
                    else:
                        pass
        
        # if text not found, fill with error text
        for str_key in ['name', 'origin', 'rank', 'fraction', 'number', 'alive', 'mode_age', 'source_rank', 'mortality_rank']:
            if str_key not in dict_data.keys():
                dict_data[str_key] = "no data found for: " + str_key

        # if object not found, fill with None
        for str_key in ['history', 'age', 'famous']:
            if str_key not in dict_data.keys():
                dict_data[str_key] = None

    return dict_data

if __name__ == "__main__":

    # get data
    dict_data = get_dict_data(res)

    # downlaod images

    str_path_img_history = os.path.join(gbl_str_path_output, gbl_str_gender + " " + str(gbl_int_rank).zfill(5) + " " + dict_data['name'] + "-history.jpg")
    str_path_img_age = os.path.join(gbl_str_path_output, gbl_str_gender + " " + str(gbl_int_rank).zfill(5) + " " + dict_data['name'] + "-age.jpg")

    urllib.request.urlretrieve(dict_data['history']['@src'], str_path_img_history)
    urllib.request.urlretrieve(dict_data['age']['@src'], str_path_img_age)

    # send email
    # https://realpython.com/python-send-email/

    sender_email = secrets.gbl_str_un

    # get receiver email from CSV
    # receiver_email = ["john_doe@gmail.com"]
    with open('/python/input/emails.csv', newline='') as f:
        reader = csv.reader(f)
        receiver_email = [row[0] for row in reader]

    message = MIMEMultipart("alternative")
    message["Subject"] = "Baby Name: " + dict_data['name']
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)

    text = """
    """ + dict_data['name'] + """
    """ + dict_data['origin']

    # name stats
    html = """\
    <html>
    <head></head>
    <body>
        <h1>""" + dict_data['name'] + """</h1>
        <b style='color:blue'><i>""" + dict_data['origin'] + """</i></b>

        <h2>Random Stats</h2>
        <ul>
            <li>""" + dict_data['rank'] + """ most popular</li>
            <li>""" + dict_data['fraction'] + """</li>
            <li>""" + dict_data['number'] + """</li>
            <li>""" + dict_data['alive'] + """</li>
            <li>""" + dict_data['mode_age'] + """</li>
        </ul>
        """

    # birth history graph
    if dict_data['history'] is not None:
        html = html + """\
        <h2>""" + dict_data['history']['@alt'] + """</h2>
        <img src="cid:image1">
        """
    
    # age distribution graph
    if dict_data['age'] is not None:
        html = html + """\
        <h2>""" + dict_data['age']['@alt'] + """</h2>
        <img src="cid:image2">
        """
    
    # famous examples
    if dict_data['famous'] is not None:
        html = html + """\
            <h2>Famous Examples</h2>
            <ul>
            """ + "\n".join(["<li>" + str_example + "</li>" for str_example in dict_data['famous']]) + """
            </ul>
            """

    # finish with Sources    
    html = html + """\
    <h2>Sources</h2>
    <ul>
        <li>""" + dict_data['source_rank'] + """</li>
        <li>""" + dict_data['mortality_rank'] + """</li>
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