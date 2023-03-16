
# Vérificateur de disponibilité de chambres Cesale

Il s'agit d'un script simple qui vérifie la disponibilité des chambres sur le site web de Cesale. Pour fonctionner, il nécessite un fichier de configuration nommé `config.json` qui doit être placé dans le répertoire racine. Le fichier doit contenir les attributs suivants :

```perl
{
    "EMAIL":"CESALE_ACCOUNT_MAIL",
    "PWD":"CESALE_ACCOUNT_PWD",
    "DATE_SORTIE":"14/02/2024",
    "NBR_LOGEMENT":"1",
    "RESIDENCES":"3,4",
    "FROM_EMAIL":"VOTRE_From_email", # configuré dans le tableau de bord SENDGRID
    "TO_EMAILS":"amirbrahamm@gmail.com",
    "SENDGRID_API_KEY":"VOTRE_API_KEY"
}
```
Pour exécuter le script en local, créez le fichier config.json et remplissez-le avec les valeurs appropriées. Ensuite, exécutez le script en utilisant un interpréteur Python.N'oublier pas de faire : 
``` pip install -r requirements.txt  ```
avant :)

Le script est hébergé sur mon compte Heroku et s'exécute toutes les heures. Il envoie un e-mail au destinataire spécifié s'il y a des chambres disponibles. L'e-mail est envoyé en utilisant SendGrid et nécessite une clé API. Vous pouvez configurer l'adresse FROM_EMAIL dans le tableau de bord SendGrid.


## ENGLISH VERSION BELOW : 

# Cesale Availability Checker

This is a simple script that checks for room availability on the Cesale website. It requires a configuration file to run, which should be named `config.json` and placed in the root directory. The file should have the following attributes:

```perl
{
    "EMAIL":"CESALE_ACCOUNT_MAIL",
    "PWD":"CESALE_ACCOUNT_PWD",
    "DATE_SORTIE":"14/02/2024",
    "NBR_LOGEMENT":"1",
    "RESIDENCES":"3,4",
    "FROM_EMAIL":"YOUR_From_email", # configured in the SENDGRID dashboard
    "TO_EMAILS":"amirbrahamm@gmail.com",
    "SENDGRID_API_KEY":"YOUR_API_KEY"
}
```

To run the script locally, create the config.json file and populate it with the appropriate values. Then, run the script using a Python interpreter.

The script is hosted on my Heroku account and executed every hour. It sends an email to the specified recipient if there are any rooms available. The email is sent using SendGrid and requires an API key. You can configure the FROM_EMAIL address in the SendGrid dashboard.
Don't forget to do 
``` pip install -r requirements.txt```  :) before running main.py

