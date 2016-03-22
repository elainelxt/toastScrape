import requests
import re
import datetime
import smtplib

login_data = {
    'name' : 'TOASTMASTERS_EMAIL',
    'password' : 'TOASTMASTERS_PASSWORD',
    'commit' : 'Log+In',                
}

url = 'http://www.supersaas.com/schedule/login/tmcs/TMCS_speaking_slots?after=%2Fschedule%2Ftmcs%2FTMCS_speaking_slots%3Fpage%3D1%26view%3Dfree'

s = requests.Session()
p = s.post( url, data = login_data)

match = re.search('var app=\[(\[.*\])\]', p.text)
if not match:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('', 'SENDER_PASSWORD')
    smtpObj.sendmail('SENDER_EMAIL', 'RECEIVER_EMAIL',
        'Subject: Update TMCS scraper\nNo match for "var app=[[...]]". Check TMCS website.')        
    smtpObj.quit()

meetings = match.group(1)
match2 = re.findall('\[(\d+),\d+,\d+,(\d+),(\d+),[^]]+\]', meetings)

available = []
for mtg in match2:
    if int(mtg[2]) < int(mtg[1]):    
        available.append(datetime.datetime.utcfromtimestamp(int(mtg[0])).strftime('%Y-%m-%d'))

if len(available) > 0:
    emailstr = 'Subject: TMCS slot available\nTMCS slot available on '
    emailstr += ', '.join(available)
    emailstr += '.\n\nBest,\nSENDER'    
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('SENDER_EMAIL', ' devworks')
    smtpObj.sendmail('SENDER_EMAIL', 'RECEIVER_EMAIL', emailstr)
    smtpObj.quit()
