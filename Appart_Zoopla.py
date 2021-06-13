import os
from bs4 import BeautifulSoup
import requests
import smtplib #send message
from email.message import EmailMessage
import csv
import pandas as pd


"""
WHY :
Being a future 2nd year Student, I was looking for an apartment to rent at the beginning of September. 
But I rapidly understood how anoying the task was (go on the website evryhour), so I thought about making a program that could go on the 
website directly for me and send me an email when a new appartment has been added.

AIM :
The program is at the end fairly simple; you just need to grab the data using bs4,then send an email. The little trick is to create a csv file within your directory.
Indeed, the program is efficient only if it runs automatically depending on the time period you want to set. So The informations about the different appartments will be stored
into this csv and a new email will be sent only if the appartment has no been added yet, hence the csv.

WARNING :
If the demand for appartment is to high, taking a google doc instead of a csv and then put it on heroku to run it every 1hour for 1 month could be beneficial.
"""




#Login, parameters already set
source = requests.get('https://www.zoopla.co.uk/to-rent/flats/fitzrovia/?beds_min=3&page_size=25&price_frequency=per_month&price_max=3000&price_min=2250&q=Fitzrovia%2C%20London&radius=0.25&results_sort=newest_listings&search_source=facets').text
soup = BeautifulSoup(source, 'html.parser') #HTML source code
# print(soup.prettify())

#How much new apparts have been added ?
New_addeds = soup.find_all('span', class_="css-gpwepq-Flag-JustAddedFlag e2uk8e17")

#
Container = soup.find('div', class_="css-kdnpqc-ListingsContainer earci3d2")
identifiers = [] #All the /to/detail/identifier

for detail in Container.find_all('a', class_='e2uk8e3 css-vhka3d-StyledLink-Link-ImageLink e33dvwd0'):
    identifiers.append(detail['href'])

# Login into each new appartment using the the identifier
    # and grab the informations from there

#Setting the emails
EMAIL_ADDRESS = os.environ.get('DB_USER')
EMAIL_PASSWORD = os.environ.get('DB_PASS')
contacts = [EMAIL_ADDRESS]
msg = EmailMessage()
msg['Subject'] = 'A New appart has been added, check it out !'
msg['From'] = EMAIL_ADDRESS #My email adress
msg['To'] = contacts # or ', '.join(contacts), same output

# Setting the csv file where all the appartment links will be put.
# The file is created so that we do not get each time the same appartment.
# When the program is running for the 2nd day in a row for instance,
    # it will write the link and send it only if the link is not already in the file, so that we get new links every time the program is run.

csv_file = open('Appart_list.csv', 'a')
writerwhite = csv.writer(csv_file)
columns = ['Appart number', 'Appart Link']
# writerwhite.writerow(columns)
df = pd.read_csv('Appart_list.csv', usecols= columns)


if len(New_addeds) >0 :

    for i in range(len(New_addeds)):
        link = f'https://www.zoopla.co.uk{identifiers[i]}'
        source2 = requests.get(link).text
        soup2 = BeautifulSoup(source2, 'html.parser')
        #Double check that it has just been added
        try:
            vac = soup2.find('span', class_="css-1j27jkb-Tag-ListingTag e1gj46vv1").text
            appart_number = identifiers[i].split('/')[3]

            if vac == 'Just added':
                msg.set_content(link)

                if int(appart_number) not in list(df['Appart number']):
                    writerwhite.writerow([appart_number, link])
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)
        except:
            print("The appart has not been 'just added' ")

csv_file.close()


