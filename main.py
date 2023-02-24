from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("chromedriver")
driver.get("https://logement.cesal-residentiel.fr/espace-resident/cesal_login.php")


elem = driver.find_element(By.ID, "button_connexion")
elem.click()


email = driver.find_element(By.ID,"login-email")
email.send_keys("gazzehhamdi4@gmail.com")

pwd = driver.find_element(By.ID,"login-password")
pwd.send_keys("An+x7bv6G")

loginButton = driver.find_elements(By.CLASS_NAME,"btn-primary")[1]
loginButton.click()
