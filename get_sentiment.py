import csv

def get_sentiment(csvfile):
    total_ingroup_sentiment = 0
    total_outgroup_sentiment = 0
    she_ingroup_sentiment = 0
    he_ingroup_sentiment = 0
    they_ingroup_sentiment = 0
    she_outgroup_sentiment = 0
    he_outgroup_sentiment = 0
    they_outgroup_sentiment = 0
    count_ingroup = 0
    count_she_ingroup = 0
    count_he_ingroup = 0
    count_they_ingroup = 0
    count_outgroup = 0
    count_she_outgroup = 0
    count_he_outgroup = 0
    count_they_outgroup = 0

    with open(csvfile, 'r') as f:
        reader = csv.DictReader(f)
        prev_tweet_id = ''
        for row in reader:
            if row["tweet_id"] != prev_tweet_id:
                #print(prev_tweet_id)
                #print(row["tweet_id"])
                #print(prev_tweet_id == row["tweet_id"])
                if row["curr_tweet_pronouns"] == row["orig_tweet_pronouns"]:
                    prev_tweet_id = row["tweet_id"]
                    count_ingroup += 1
                    total_ingroup_sentiment += float(row["curr_tweet_sentiment"])
                    if row["curr_tweet_pronouns"] == "she":
                        count_she_ingroup += 1
                        she_ingroup_sentiment += float(row["curr_tweet_sentiment"])
                    elif row["curr_tweet_pronouns"] == "he":
                        count_he_ingroup += 1
                        he_ingroup_sentiment += float(row["curr_tweet_sentiment"])
                    elif row["curr_tweet_pronouns"] == "they":
                        count_they_ingroup += 1
                        they_ingroup_sentiment += float(row["curr_tweet_sentiment"])
                elif row["curr_tweet_sentiment"] != "curr_tweet_sentiment":
                    prev_tweet_id = row["tweet_id"]
                    count_outgroup += 1
                    total_outgroup_sentiment += float(row["curr_tweet_sentiment"])
                    if row["curr_tweet_pronouns"] == "she":
                        print(row["tweet_text"])
                        print(row["curr_tweet_sentiment"])
                        count_she_outgroup += 1
                        she_outgroup_sentiment += float(row["curr_tweet_sentiment"])
                    elif row["curr_tweet_pronouns"] == "he":
                        count_he_outgroup += 1
                        he_outgroup_sentiment += float(row["curr_tweet_sentiment"])
                    elif row["curr_tweet_pronouns"] == "they":
                        count_they_outgroup += 1
                        they_outgroup_sentiment += float(row["curr_tweet_sentiment"])

    print("ingroup total: " + str(total_ingroup_sentiment/count_ingroup))
    print("ingroup she: " + str(she_ingroup_sentiment/count_she_ingroup))
    print("ingroup he: " + str(he_ingroup_sentiment/count_he_ingroup))
    print("ingroup they: " + str(they_ingroup_sentiment/count_they_ingroup))
    print("outgroup total: " + str(total_outgroup_sentiment/count_outgroup))
    print("outgroup she: " + str(she_outgroup_sentiment/count_she_outgroup))
    print("outgroup he: " + str(he_outgroup_sentiment/count_he_outgroup))
    print("outgroup they: " + str(they_outgroup_sentiment/count_they_outgroup))

get_sentiment("pronouns_partial.csv")
