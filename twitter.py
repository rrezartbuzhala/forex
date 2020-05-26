from twitterscraper import query_tweets_from_user
from time import sleep
from colorama import Fore, Back, Style 
import pyodbc 
import uuid

#lang = "english"

#Connection with DB
conn = pyodbc.connect('Driver={SQL Server};''Server=RREZARTPC\SQLEXPRESS;''Database=Forliza2;''Trusted_Connection=yes;')
cursor = conn.cursor()

def get_keywords_in_tweet(tweet):
    keywords_select = cursor.execute('select keyword from Keywords').fetchone()
    keywords = []
    for keyword in keywords_select:
        keywords.append(keyword)
        # TO DO:  if keyword in tweet, add keyword to keywords list
    return keywords


while True:
    #Retriving analyst usernames and Guids from DB
    analysts_usernames = []
    analysts_id = []
    analystsSelect = cursor.execute('select Username,Id from Analysts').fetchall()
    for analyst_username in analystsSelect:
        analysts_usernames.append(analyst_username.Username)
        analysts_id.append(analyst_username.Id)

    #Adding tweets in DB...
    for (analyst_username,analyst_id) in zip(analysts_usernames,analysts_id):
        list_of_tweets =  query_tweets_from_user(analyst_username, limit = 1)
        if list_of_tweets == []:
            print(Fore.RED+"Private user or no post")
            print(Fore.RESET)
            continue
        last_tweet = list_of_tweets[0]
        try:
            inserted_last_tweet = cursor.execute("select top 1 Tweet from AnalystTweets where Analyst_Id = '"+analyst_id+"' order by Added_At desc").fetchone()
        except TypeError:
            inserted_last_tweet = ('',)
            
        if inserted_last_tweet != None:
            inserted_last_tweet = inserted_last_tweet.Tweet

        if last_tweet.screen_name == analyst_username and last_tweet.text != inserted_last_tweet:
            params = (analyst_id,last_tweet.text,str(uuid.uuid4()))
            conn.execute("{CALL InsertTweets (?,?,?)}", params)
            conn.commit()
            keywords = get_keywords_in_tweet(params[1])
            for keyword in keywords:
                params = [keyword,params[2]]
                conn.execute("{CALL InsertTweetsWithKeywords (?,?)}", params)

    sleeptime = 20
    sleep(sleeptime)
    # for i in range(sleeptime):
    #     print(i+1)
    #     sleep(1)
            