from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from bs4 import BeautifulSoup

import json
import os
import requests
# ------------CONFIG START ----------------------
URL = "https://ibail.arpej.fr/residences/SA/reservation-d-un-logement" # SA pour les logements à Alexandre Manceau

VERBOSE = False
if ("ON_HEROKU" in os.environ):
    try:
        FROM_EMAIL = os.environ.get("FROM_EMAIL")
        TO_EMAILS = os.environ.get("TO_EMAILS").split(",")
        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    except:
        print("something went wrong loading ENV variables , exiting..")
        exit()
else:
    if (not os.path.exists("config.json")):
        print("you are running this script locally , please include a config.json on next launch")
        exit()
    try:
        f = open("config.json")
        data = json.load(f)
        FROM_EMAIL = data["FROM_EMAIL"]
        TO_EMAILS = data["TO_EMAILS"].split(",")
        SENDGRID_API_KEY = data["SENDGRID_API_KEY"]
    except:
        print("something went wrong loading config.json , exiting..")
        exit()
# ------------CONFIG END ----------------------


def send_email(emails, notification_text, subject):
    html_content = '<strong>' + notification_text + '</strong>'
    emails = emails
    message = Mail(
        from_email='amirbrahamm@gmail.com',
        to_emails=emails,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return "Email Sent"
    except Exception as e:
        return e.message

token = "f8a088b7bc7896705b0a26a90c625f670acc15f299d20db2cddce08a3d1d7709"
headersAPI = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+token,
}

def main():
    try:
        res = requests.get("https://admin.arpej.fr/api/customer/residences/59/availabilities/2023-03/offers",headers=headersAPI)
        data = res.json()
        f = open("arpej.json")
        oldData = json.load(f)
        f.close()
        if(oldData == data):
            print("Pas de nouveau Logement pour Amir , le pauvre :/ ")
        else:
            content = json.dumps(data)
            print("sending mail right now !! ")
            send_email([TO_EMAILS[0]], content, "Logement Aprej Trouvé")
            f = open("arpej.json","w")
            f.write(content)
            f.close() # Close file
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()