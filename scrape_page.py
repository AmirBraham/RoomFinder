from bs4 import BeautifulSoup
import re

f = open("index.php")
soup = BeautifulSoup(f, 'html.parser')

logements = soup.find_all ("tr",id=re.compile("r_logement_"))
for logement in logements:
    tds = logement.children
    for td in tds:
        print(td)