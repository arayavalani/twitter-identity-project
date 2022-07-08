import tweepy, json
import os
from unidecode import unidecode
from datetime import date
import gzip

def print_all_keys(d, prefix=""):
    for key, value in d.items():
        if isinstance(value, dict):
            print_all_keys(value, prefix + str(key) + ".")
        else:
            print(prefix + key)



class streamtweets(tweepy.Stream):
    def on_status(self, status):
        #print_all_keys(status._json)
        '''
        with open('teststream.csv', 'a', encoding = 'utf-8') as w:
            tweet_text = status._json['text']
            user_name = status._json['user']['name']
            user_bio = status._json['user']['description']
            tweet_id = str(status._json['id'])
            if user_bio == None:
                user_bio = "None"
            w.write(tweet_text + "\t" + user_name + "\t" + user_bio + "\t" + tweet_id + "\t")
        '''
        # get current datetime and create a filename with it
        today = date.today()
        filename = today.strftime("%m-%d-%Y")
        cwd = os.path.abspath(os.getcwd())

        with gzip.open("/projects/p31502/projects/twitter_corpus/tweets/tweets-" + filename + '.jsonl.gz','at') as w:
            json_out = status._json
            #print(status._json["id"])

            # unidecode all user-input text fields
            # also for quoted & retweeted users

            # top level tweet
            json_out['text'] = unidecode(json_out['text'], errors='preserve')
            json_out['user']['name'] = unidecode(json_out['user']['name'], errors='preserve')

            if json_out['user']['description'] != None:
                json_out['user']['description'] = unidecode(json_out['user']['description'], errors='preserve')

            if json_out['user']['location'] != None:
                json_out['user']['location'] = unidecode(json_out['user']['location'], errors='preserve')

            # does it quote any tweets? does the quoted tweet still exist (not deleted)
            if json_out['is_quote_status'] == True and 'quoted_status' in json_out.keys():
                json_out['quoted_status']['text'] = unidecode(json_out['quoted_status']['text'], errors='preserve')
                if json_out['quoted_status']['user']['description'] != None:
                    json_out['quoted_status']['user']['description'] = unidecode(json_out['quoted_status']['user']['description'], errors='preserve')
                if json_out['quoted_status']['user']['location'] != None:
                    json_out['quoted_status']['user']['location'] = unidecode(json_out['quoted_status']['user']['location'], errors='preserve')

            # is it retweeting something?
            # text begins with "RT @"
            if json_out['text'].startswith('RT @') == True and 'retweeted_status' in json_out.keys():
                json_out['retweeted_status']['text'] = unidecode(json_out['retweeted_status']['text'], errors='preserve')                
                if json_out['retweeted_status']['user']['description'] != None:
                    json_out['retweeted_status']['user']['description'] = unidecode(json_out['retweeted_status']['user']['description'], errors='preserve')
                if json_out['retweeted_status']['user']['location'] != None:
                    json_out['retweeted_status']['user']['location'] = unidecode(json_out['retweeted_status']['user']['location'], errors='preserve')
                # does that retweet have yet another quote tweet?
                if json_out['retweeted_status']['is_quote_status'] == True and 'quoted_status' in json_out['retweeted_status'].keys(): 
                    json_out['retweeted_status']['quoted_status']['text'] = unidecode(json_out['retweeted_status']['quoted_status']['text'], errors='preserve')                
                    if json_out['retweeted_status']['quoted_status']['user']['description'] != None:
                        json_out['retweeted_status']['quoted_status']['user']['description'] = unidecode(json_out['retweeted_status']['quoted_status']['user']['description'], errors='preserve')
                    if json_out['retweeted_status']['quoted_status']['user']['location'] != None:
                        json_out['retweeted_status']['quoted_status']['user']['location'] = unidecode(json_out['retweeted_status']['quoted_status']['user']['location'], errors='preserve')

            w.write(json.dumps(json_out) + '\n')


        #print(status._json['text'])
        #print(status._json['id'])

if __name__ == "__main__":
    # keys from vlab github
    api_key = 'eWzVNQc0AsmjTnSHfqtImUWhj'
    api_secret = 'mwieBPcAyxZxLxJhixayEWuGmGoNv6ZjAspwBWO0smnq3GVUyc'
    access_token = '1407003631535206405-usR9tixZJQRFJ9nJIuYTueGd0HJaCz'
    secret_token = '8bv9G9UTcSdX3wT5vpZycDAWmVLS9XzsFq1tnLYJCVP41'

    streamer = streamtweets(api_key, api_secret, access_token, secret_token)

    streamer.sample(languages=['en'])
