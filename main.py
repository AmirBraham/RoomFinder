from selenium import webdriver
from selenium.webdriver.common.by import By
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import pandas as pd
import os
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
#------------CONFIG START ----------------------
HEADLESS = True
if("ON_HEROKU" in os.environ):
    try:
        EMAIL = os.environ.get("EMAIL")
        PWD = os.environ.get("PWD")
        DATE_SORTIE = os.environ.get("DATE_SORTIE")
        NBR_LOGEMENT = int(os.environ.get("NBR_LOGEMENT"))
        RESIDENCES = os.environ.get("RESIDENCES").split(",")
        FROM_EMAIL = os.environ.get("FROM_EMAIL")
        TO_EMAILS = os.environ.get("TO_EMAILS").split(",")
        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    except:
        print("something went wrong loading ENV variables , exiting..")
        exit()
else:
    if(not os.path.exists("config.json")):
        print("you are running this script locally , please include a config.json on next launch")
        exit()
    try:
        f = open("config.json")
        data = json.load(f)
        EMAIL = data["EMAIL"]
        PWD = data["PWD"]
        DATE_SORTIE = data["DATE_SORTIE"]
        NBR_LOGEMENT = int(data["NBR_LOGEMENT"])
        RESIDENCES = data["RESIDENCES"].split(",")
        FROM_EMAIL = data["FROM_EMAIL"]
        TO_EMAILS = data["TO_EMAILS"].split(",")
        SENDGRID_API_KEY = data["SENDGRID_API_KEY"]
    except:
        print("something went wrong loading config.json , exiting..")
        exit()
#------------CONFIG END ----------------------


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
if(HEADLESS):
   options.add_argument("--headless=new")
if("ON_HEROKU" in os.environ):
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome("chromedriver",options=options)

driver.get("https://logement.cesal-residentiel.fr/espace-resident/cesal_login.php")


elem = driver.find_element(By.ID, "button_connexion")
elem.click()

print("signing in")
email = driver.find_element(By.ID,"login-email")
email.send_keys(EMAIL)

pwd = driver.find_element(By.ID,"login-password")
pwd.send_keys(PWD)

loginButton = driver.find_elements(By.CLASS_NAME,"btn-primary")[1]
loginButton.click()
print("login done , going to reservation page")
driver.get("https://logement.cesal-residentiel.fr/espace-resident/cesal_mon_logement_reservation.php")

print("setting date_arrivee")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "date_arrivee")))
el = driver.find_element(By.ID,"date_arrivee")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "option")))
option = el.find_elements(By.TAG_NAME,'option')[-1]
option.click()

print("setting date_sortie")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID,"date_sortie")))

bail = driver.find_element(By.ID,"date_sortie")
bail.send_keys(DATE_SORTIE)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,"btn-success")))

buttons = driver.find_elements(By.CLASS_NAME,"btn-success")
valider_button = None
for b in buttons:
    if(b.get_attribute('innerText') == "Valider"):
        valider_button = b

import time
time.sleep(3)
if(valider_button is not None):
    valider_button.click()

else:
    print("something went wrong , exiting...")
    exit()

print("fetching reservation page")

WebDriverWait(driver, 100).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

with open("index.php", "w", encoding='utf-8') as f:
    f.write(driver.page_source)
print("scraping reservation page")

dfs = pd.read_html("index.php", encoding='utf-8')

results = []
for df in dfs:
    df.columns = df.columns.str.replace('°', '')
    df.columns = df.columns.str.replace('º', '')
    if ("N Logement" not in df or "Nbr occupantslogement" not in df):
        continue
    df = df[(df['Nbr occupantslogement'] == NBR_LOGEMENT)]
    def filterResidences(df):
        t = tuple(RESIDENCES)
        df = df[df['N Logement'].str.startswith(t)]
        return df
    df = filterResidences(df=df)
    if (df.empty):
        continue
    results.append(df)


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


if (len(results) > 0):
    # YAY , on a trouvé une chambre : envoie du mail :
    MESSAGE = """"""
    for df in results:
        MESSAGE += df.to_html()
        MESSAGE += "\n ------------------------- \n"
    print(MESSAGE)
    print("sending mail right now !! ")
    send_email(["amirbrahamm@gmail.com"],MESSAGE,"Logement Césale Trouvé")
else:
    print("pas de logement , Amir le pauvre :\\")

driver.close()