import json
import os
import requests
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import pandas as pd

# ------------CONFIG START ----------------------
VERBOSE = False
if ("ON_HEROKU" in os.environ):
    try:
        EMAIL = os.getenv("cesale_mail")
        PWD = os.getenv("cesale_mdp")
        NBR_LOGEMENT = int(os.getenv("NBR_LOGEMENT"))
        RESIDENCES = os.getenv("RESIDENCES").split(",")
        FROM_EMAIL = os.getenv("FROM_EMAIL")
        TO_EMAILS = os.getenv("TO_EMAILS").split(",")
        SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
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
        EMAIL = data["EMAIL"]
        PWD = data["PWD"]
        NBR_LOGEMENT = int(data["NBR_LOGEMENT"])
        RESIDENCES = data["RESIDENCES"].split(",")
        FROM_EMAIL = data["FROM_EMAIL"]
        TO_EMAILS = data["TO_EMAILS"].split(",")
        SENDGRID_API_KEY = data["SENDGRID_API_KEY"]
    except:
        print("something went wrong loading config.json , exiting..")
        exit()
# ------------CONFIG END ----------------------


LOGIN_URL = "https://logement.cesal-residentiel.fr/espace-resident/cesal_login.php"
URL = "https://logement.cesal-residentiel.fr/espace-resident/cesal_mon_logement_reservation.php"


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


def main():
    session_requests = requests.session()
    # Create payload
    login_payload = {
        "action": "login",
        "login-email": EMAIL,
        "login-password": PWD
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
         
          'referer': LOGIN_URL}
    cookies = {
        "_ga": "GA1.2.1938810788.1678984314",
        "_gid": "GA1.2.1032678773.1678984314",
        "CESAL_RESIDENTIEL_LOGEMENT": "kr820bgmah2h6cu8ragri39m2a",
        "CSLAC_RESIDENTIEL_LOGEMENT": "321065432106543210654321065XU",
        "_gat_gtag_UA_144222640_2": "1"
    }
    
    # Perform login
    print("login payload : ")
    print(login_payload)
    result = session_requests.post(
        LOGIN_URL, data=login_payload,cookies=cookies, headers=headers)

    res = session_requests.get(URL,cookies=cookies, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    select = soup.find('select', attrs={'name': 'date_arrivee'})
    if (select is None):
        print("error finding select , exiting ..")
        exit()
    subject_options = [i.get_text()
                       for i in select.findChildren("option") if i != "\n" and i]
    if (len(subject_options) < 2):
        print("something went wrong ")
        print(subject_options)
        exit()
    date_arrivee = subject_options[-1]
    date_arrivee = datetime.strptime(date_arrivee, "%d/%m/%Y")
    date_sortie = date_arrivee + relativedelta(months=10)
    print("date_arrivee : " + str(date_arrivee.date()))
    print("date_sortie : " + str(date_sortie.date()))
    reservation_payload = {
        "action": "modifier_date_arrivee",
        "date_arrivee": str(date_arrivee.date()),
        "date_sortie": str(date_sortie.date())
    }
    # Scrape url
    result = session_requests.post(
        URL,cookies=cookies, data=reservation_payload,  headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    with open("index.php", "w", encoding='utf-8') as f:
        f.write(str(soup))

    dfs = pd.read_html("index.php", encoding='utf-8')

    results = []
    for df in dfs:
        df.columns = df.columns.str.replace('°', '')
        df.columns = df.columns.str.replace('º', '')

        if ("N Logement" not in df or "Nbr occupants logement" not in df):
            continue
        df = df[(df['Nbr occupants logement'] == NBR_LOGEMENT)]

        def filterResidences(df):
            t = tuple(RESIDENCES)
            df = df[df['N Logement'].str.startswith(t)]
            return df
        df = filterResidences(df=df)
        if (df.empty):
            continue

        results.append(df)

    if (len(results) > 0):
        # YAY , on a trouvé une chambre : envoie du mail :
        MESSAGE = """"""
        for df in results:
            MESSAGE += df.to_html()
            MESSAGE += "\n ------------------------- \n"
        print("sending mail right now !! ")
        send_email(TO_EMAILS, MESSAGE, "Logement Césale Trouvé")
    else:
        print("pas de logement , Amir le pauvre :\\")


main()
