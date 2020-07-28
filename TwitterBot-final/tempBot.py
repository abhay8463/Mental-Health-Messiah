import tweepy, random, time
# from our keys module (keys.py), import the keys dictionary
from keys import keys
import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import numpy as np
import re
import preprocessor as p
import reddit_twitter_bot

'''Twitter Auth'''
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
IBM_KEY = keys['ibm_key']
IBM_URL = keys['ibm_url']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

'''IBM Auth'''
authenticator = IAMAuthenticator(IBM_KEY)
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
tone_analyzer.set_service_url(IBM_URL)

prev_id = ""
with open('prev_id_temp.txt', 'r') as f:
    for line in f:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]

        # add item to the list
        prev_id = currentPlace
        print("last prev id from memory: - ", prev_id)
        print(type(prev_id))
i = 0
while True:
    i += 1
    print("debugCounter = ", i)
    twt = api.search("#Covid19", result_type="new", count=1)
    for t in twt:
        print("debug: - ", t.id, prev_id, type(t.id), t.text, t.user.screen_name)
        if str(t.id) != str(prev_id):
            if (not t.retweeted) and ('RT @' not in t.text):
                print("tweet text: ", t.text)
                prev_id = t.id
                with open('prev_id_temp.txt', 'w') as f:
                    f.write('%s\n' % prev_id)
                '''Tone Analyzing'''
                tone_analysis = tone_analyzer.tone(
                    {'text': t.text},
                    content_type='application/json'
                ).get_result()
                print("debug\n", tone_analysis)
                try:
                    tone = tone_analysis['document_tone']['tones'][0]['tone_id']
                    print("Tone detected: - ", tone, "\n\n")
                    if tone.lower() == "sadness":
                        title, link, extension = reddit_twitter_bot.findMeme()
                        status = "Hey @" + t.user.screen_name + " This is a mini project. Please read bio for more info\n Our sentimental bot detected your depressed tweet :(\nHere's a motivational quote for you: -\n" + title + "\n" + "https://redd.it/" + link
                        imagePath = "img\\output" + extension
                        print("debug: ", t.text)
                        print(type(t.id))
                        print(type(t.id_str))
                        print(t.id, " debug ends")
                        # sn = t.user.screen_name
                        # m = "@%s " % sn + "Hello,"
                        # api.update_status(status=m, in_reply_to_status_id=t.id_str)
                        api.update_with_media(imagePath, status, in_reply_to_status_id=t.id)
                except:
                    print("No tone detected")
            else:
                print("skipping cause retweet.")
    time.sleep(120)

    # for t in twt:
    #     if t.text.find("#covid19") != -1:
    #         title, link, extension = reddit_twitter_bot.findMeme()
    #         status = "Hey @" + t.user.screen_name + " Our sentimental bot detected your depressed tweet :(\nHere's a motivational quote for you: -\n" + title + "\n" + "https://redd.it/" + link
    #         imagePath = "img\\output" + extension
    #         print(t.text)
    #         print(type(t.id))
    #         print(type(t.id_str))
    #         print(t.id)
    #         # sn = t.user.screen_name
    #         # m = "@%s " % sn + "Hello,"
    #         # api.update_status(status=m, in_reply_to_status_id=t.id_str)
    #         api.update_with_media(imagePath, status, in_reply_to_status_id=t.id)
