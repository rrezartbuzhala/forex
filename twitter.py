from twitterscraper import query_tweets_from_user
from time import sleep
from colorama import Fore, Back, Style 
from datetime import date
import pyodbc 
import uuid
import copy

#lang = "english"

#Connection with DB
conn = pyodbc.connect('Driver={SQL Server};''Server=RREZARTPC\SQLEXPRESS;''Database=Forliza;''Trusted_Connection=yes;')
cursor = conn.cursor()

class Keyword:
    def __init__(self, id, keyword):
        self.id = id
        self.keyword = keyword

def get_keywords_in_tweet(tweet):
    keywords_select = cursor.execute('select * from Keywords').fetchall()
    keywords = []
    for keyword in keywords_select:
        keywords.append(Keyword(keyword.Id,keyword.Keyword))
    result = []
    for keyword in keywords:
        # keyword_variations = [keyword.keyword.lower(),keyword.keyword.upper(),keyword.keyword.capitalize()]
        # keyword_in_tweet = False
        # for _keyword in keyword_variations:
        #     if _keyword in tweet:
        #         keyword_in_tweet = True
        #         break
        if keyword.keyword.lower() in tweet.lower():
            result.append(keyword) 
    return result
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
        # TODO : Add a boolean to tell if a tweet with the same text exists in DB
        if last_tweet.screen_name == analyst_username and last_tweet.text != inserted_last_tweet:
            tweet_id = str(uuid.uuid4())
            params = (tweet_id,analyst_id,last_tweet.text,date.Today(),date.Today())
            print(params[0])
            conn.execute("{CALL InsertTweets (?,?,?,?,?)}", params)
            conn.commit()
            keywords = get_keywords_in_tweet(last_tweet.text)
            for keyword in keywords:
                params = [tweet_id,keyword.id]
                print(params[0])
                conn.execute("{CALL InsertTweetsWithKeywords (?,?)}", params)
                conn.commit()

    sleeptime = 1
    sleep(sleeptime)
    # for i in range(sleeptime):
    #     print(i+1)
    #     sleep(1)
            
