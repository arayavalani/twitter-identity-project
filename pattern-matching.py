import json
import re
import os
import tweepy
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def match_bio_and_text(directory, patterns):
#    for input_file in os.listdir(directory):
    with open(input_file, 'r') as file:
        for tweet in file:
            tweet_json = json.loads(tweet)
            for pattern in patterns:
                # no retweets
                if str(tweet_json["text"])[0:4] != "RT @" and re.search(pattern, str(tweet_json["user"]["description"])) and re.search(pattern, str(tweet_json["text"])):
                    print("tweet id: " + str(tweet_json["id"]))
                    print("user bio: " + str(tweet_json["user"]["description"]))
                    print("tweet text: " + tweet_json["text"])


def find_bio(input_file, patterns):
    with open(input_file, 'r') as file:
        for tweet in file:
            tweet_json = json.loads(tweet)
            for pattern in patterns:
                if re.search(pattern, str(tweet_json["user"]["description"])):
                    print("tweet id: " + str(tweet_json["id"]))
                    print("user bio: " + str(tweet_json["user"]["description"]))
                    print("tweet text: " + tweet_json["text"])

def match_bio_and_OP_bio(directory, patterns):
    api_key = 'eWzVNQc0AsmjTnSHfqtImUWhj'
    api_secret = 'mwieBPcAyxZxLxJhixayEWuGmGoNv6ZjAspwBWO0smnq3GVUyc'
    access_token = '1407003631535206405-usR9tixZJQRFJ9nJIuYTueGd0HJaCz'
    secret_token = '8bv9G9UTcSdX3wT5vpZycDAWmVLS9XzsFq1tnLYJCVP41'

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, secret_token)
    api = tweepy.API(auth, wait_on_rate_limit = True, retry_count=10, retry_delay=5, retry_errors=set([503, 104]))

    file_number = 0
    for input_file in os.listdir(directory):
        with open(tweets_dir + input_file, 'r') as tweets_file:
            with open('pronouns.csv', 'a') as results_csv:
                fieldnames = ['reply_pronouns', 'reply_sentiment', 'parent_pronouns', 'parent_sentiment', 'tweet_id', 'user_bio', 'user_name', 'tweet_text', 'parent_tweet_id', 'parent_user_bio', 'parent_user_name', 'parent_tweet_text']
                writer = csv.DictWriter(results_csv, fieldnames=fieldnames)
                if file_number == 0:
                    writer.writeheader()
 
                # prevent duplicates in csv
                prev_tweet_id = ''
                for tweet in tweets_file:
                    tweet_json = json.loads(tweet)
                    for pattern in patterns:
                        # first char: @ = reply
                        if str(tweet_json["text"])[0] == "@" and re.search(pattern, str(tweet_json["user"]["description"])):
                            try:                            
                                parent_tweet = api.get_status(tweet_json["in_reply_to_status_id"], tweet_mode='extended')
                                for parent_pattern in patterns:
                                    if re.search(parent_pattern, str(parent_tweet._json["user"]["description"])):
                                        if pattern == '([Hh]e[\W]*[Hh]im)':
                                            pronoun = "he"
                                        elif pattern == '([tT]hey[\W]*[tT]hem)':
                                            pronoun = "they"
                                        elif pattern == '([sS]he[\W]*[hH]er)':
                                            pronoun = "she"

                                        if parent_pattern == '([Hh]e[\W]*[Hh]im)':
                                            parent_pronoun = "he"
                                        elif parent_pattern == '([tT]hey[\W]*[tT]hem)':
                                            parent_pronoun = "they"
                                        elif parent_pattern == '([sS]he[\W]*[hH]er)':
                                            parent_pronoun = "she"
                                       
                                        analyzer = SentimentIntensityAnalyzer()
                                        reply_vs = analyzer.polarity_scores(tweet_json["text"])
                                        parent_vs = analyzer.polarity_scores(parent_tweet._json["text"])
                                        # if compound score is 0.0, neu==1.0, can't classify sentiment
                                        if reply_vs["compound"] != 0.0 and parent_vs["compound"] != 0.0:
                                            if tweet_json["id"] != prev_tweet_id:
                                                print("tweet id: " + str(tweet_json["id"]))
                                                writer.writerow({"reply_pronouns": pronoun, "reply_sentiment": reply_vs["compound"], "parent_pronouns": parent_pronoun, "parent_sentiment": parent_vs["compound"], "tweet_id": "\"" + str(tweet_json["id"]) + "\"", "user_bio": str(tweet_json["user"]["description"]), "user_name": str(tweet_json["user"]["name"]) + " " + str(tweet_json["user"]["screen_name"]), "tweet_text": tweet_json["text"], "parent_tweet_id": "\"" + str(parent_tweet._json["id"]) + "\"", "parent_user_bio": str(parent_tweet._json["user"]["description"]), "parent_user_name": str(parent_tweet._json["user"]["name"]) + " " + str(parent_tweet._json["user"]["screen_name"]), "parent_tweet_text": parent_tweet._json["text"]})
                                                prev_tweet_id = tweet_json["id"]
                            except tweepy.errors.Forbidden as e:
                                pass
                            except tweepy.errors.NotFound as e:
                                pass
        file_number += 1                       

         
                            #print("original tweet id: " + str(orig_tweet._json["id"]))
                            #print("original user bio: " + str(orig_tweet._json["user"]["description"]))
                            #print("original user name: " + str(orig_tweet._json["user"]["name"]) + " " + str(orig_tweet._json["user"]["screen_name"]))
                            #print("original tweet text: " + orig_tweet._json["text"])



tweets_dir = '/projects/p31502/projects/twitter_corpus/tweets/'



match_bio_and_OP_bio(tweets_dir, ['([Hh]e[\W]*[Hh]im)', '([tT]hey[\W]*[tT]hem)', '([sS]he[\W]*[hH]er)'])

#find_bio_and_text('tweets-01-03-2022.jsonl', ['([\W ][pP][oO][cC][\W ])','([\W ][bB][iI][pP][oO][cC][\W ])', '[\W ][sS]tudent[\W ]', '[\W ][hH]usband[\W ]', '[\W ][fF]ather[\W ]', '[\W ][wW]ife[\W ]', '[\W ][mM]other[\W ]', '[\W ][aA]utistic[\W ]', '[\W ][vV]egan[\W ]', '[\W ][cC]hristian[\W ]', '[\W ][gG]ay[\W ]', '[\W ][lL]esbian[\W ]', '[\W ][tT]rans[\W ]', '[\W ][lL]eftist[\W ]', '[\W ][cC]onservative[\W ]', '[\W ][lL]iberal[\W ]', '([\W ][tT][eE][rR][fF][\W ])'])

# from paper
# \ba*h+a+h+a+(h+a+)*?h*\b|\bl+o+l+(o+l+)*?\b|\bh+e+h+e+(h+e+)*?h*\b
# (hah), lo+l+, (lm)a+o+
# keysmash laughter

# patterns: "I am a [...] but" outside quotation marks (coming from user)
#find_patterns('tweets-01-02-2022.jsonl', ['(I am a )+(.*?)\s+(but)(?=([^"]*"[^"]*")*[^"]*$)', '(I\'m a )+(.*?)\s+(but)(?=([^"]*"[^"]*")*[^"]*$)', '(I am an )+(.*?)\s+(but)(?=([^"]*"[^"]*")*[^"]*$)', '(I\'m an )+(.*?)\s+(but)(?=([^"]*"[^"]*")*[^"]*$)'])

# as a... I think
