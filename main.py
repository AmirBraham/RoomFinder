from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome("chromedriver",options=options)

driver.get("https://logement.cesal-residentiel.fr/espace-resident/cesal_login.php")


elem = driver.find_element(By.ID, "button_connexion")
elem.click()


email = driver.find_element(By.ID,"login-email")
email.send_keys("gazzehhamdi4@gmail.com")

pwd = driver.find_element(By.ID,"login-password")
pwd.send_keys("An+x7bv6G")

loginButton = driver.find_elements(By.CLASS_NAME,"btn-primary")[1]
loginButton.click()

driver.get("https://logement.cesal-residentiel.fr/espace-resident/cesal_mon_logement_reservation.php")


el = driver.find_element(By.ID,"date_arrivee")

option = el.find_elements(By.TAG_NAME,'option')[-1]
option.click()


bail = driver.find_element(By.ID,"date_sortie")
bail.send_keys("01/03/2024")

button = driver.find_elements(By.CLASS_NAME,"btn-success")[1]
button.click()



with open("index.php", "w", encoding='utf-8') as f:
    f.write(driver.page_source)

driver.close()