from twitterscraper import query_tweets_from_user
from time import sleep
from colorama import Fore, Back, Style 
import pyodbc 
import uuid

#lang = "english"

#Connection with DD
conn = pyodbc.connect('Driver={SQL Server};''Server=RREZARTPC\SQLEXPRESS;''Database=Forliza2;''Trusted_Connection=yes;')
cursor = conn.cursor()

def find_keywords_in_tweets():
    keywords_select = cursor.execute('select * from Keywords').fetchall()
    #

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
            inserted_last_tweet = cursor.execute("select top 1 Tweet from AnalystTweets where AnalystID = '"+analystID+"' order by Id desc").fetchone()
        except TypeError:
            inserted_last_tweet = ('',)
            
        if inserted_last_tweet != None:
            inserted_last_tweet = inserted_last_tweet.Tweet

        if last_tweet.screen_name == analyst and last_tweet.text != inserted_last_tweet:
            params = (analystID,last_tweet.text, str(uuid.uuid4()))
            conn.execute("{CALL InsertTweets (?,?,?)}", params)
            conn.commit()
    sleeptime = 20
    sleep(sleeptime)
    # for i in range(sleeptime):
    #     print(i+1)
    #     sleep(1)
            