from twitterscraper import query_tweets_from_user
from time import sleep
from colorama import Fore, Back, Style 
import pyodbc 

#lang = "english"

#Connection with DD
conn = pyodbc.connect('Driver={SQL Server};''Server=DESKTOP-585PVI8;''Database=Forliza2;''Trusted_Connection=yes;')
cursor = conn.cursor()


while True:
    #Retriving analyst usernames and Guids from DB
    analysts = []
    analystsID = []
    analystsSelect = cursor.execute('select Username,Id from Analysts').fetchall()
    for analyst in analystsSelect:
        analysts.append(analyst.Username)
        analystsID.append(analyst.Id)

    #Adding tweets in DB...
    for (analyst,analystID) in zip(analysts,analystsID):
        list_of_tweets =  query_tweets_from_user(analyst, limit = 1)
        if list_of_tweets == []:
            print(Fore.RED+"Private user or no post")
            print(Fore.RESET)
            continue
        last_tweet = list_of_tweets[0]
        try:
            inserted_last = cursor.execute("select top 1 Tweet from AnalystTweets where AnalystID = '"+analystID+"' order by Id desc").fetchone()
        except TypeError:
            inserted_last = ('',)
            
        if inserted_last != None:
            inserted_last = inserted_last.Tweet

        if last_tweet.screen_name == analyst and last_tweet.text != inserted_last:
            params = (analystID,last_tweet.text)
            conn.execute("{CALL InsertTweets (?,?)}", params)
            conn.commit()

    sleeptime = 1
    sleep(sleeptime)
    # for i in range(sleeptime):
    #     print(i+1)
    #     sleep(1)
            