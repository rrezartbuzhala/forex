from twitterscraper import query_tweets_from_user
import datetime as dt
import pyodbc 

#lang = "english"

#Connection with DD
conn = pyodbc.connect('Driver={SQL Server};''Server=DESKTOP-585PVI8;''Database=Forliza;''Trusted_Connection=yes;')
cursor = conn.cursor()

#Retriving analyst usernames from DB
analysts = []
analystsSelect = cursor.execute('select Username from Analysts')
for analyst in analystsSelect:
    analysts.append(analyst.Username)

#Adding tweets in DB...
for analyst in analysts:
    list_of_tweets =  query_tweets_from_user(analyst, limit = 10)
    for tweet in list_of_tweets:
        originalTweet = False
        #...only the original tweets
        for analyst in analysts:
            if tweet.screen_name == analyst:
                originalTweet = True
                break
        if originalTweet:
            params = (tweet.username,tweet.screen_name,tweet.text)
            conn.execute("{CALL InsertTweets (?,?,?)}", params)
            conn.commit()


        

