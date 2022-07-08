import spacy
from spacy.matcher import DependencyMatcher
import re

# [json processing stuff]
# from json get text of each tweet
# search tweet text for hearst pattern
# for each tweet regex search for any hearst pattern
# if hearst pattern found: (else continue)
# depending on which pattern it is, do dependency parsing accordingly to find NP

# take body of each tweet, regex search for each hearst pattern
def search_for_pattern(input_text, identity_patterns):
    found_patterns = []
    for pattern in identity_patterns:
        match = re.search(pattern, input_text)
        if match:
            found_patterns.append((pattern, match.span()))
    return found_patterns

# take found hearst patterns and extract NP 
def dependency_parsing(input_text, found_patterns):
    nlp = spacy.load("en_core_web_sm")
    matcher = DependencyMatcher(nlp.vocab)
    # "as a(n) X", we want the child(object) of "as"
    # along with any modifiers, prepositions, etc. of that object
    # how to make modifier optional?

    # as a [modifier] [object]
    as_pattern = [
    {
        "RIGHT_ID": "anchor_as",
        "RIGHT_ATTRS": {"ORTH": "as"}
    },
    {
        "LEFT_ID": "anchor_as",
        "REL_OP": ">",
        "RIGHT_ID": "as_object",
        "RIGHT_ATTRS": {"DEP": "pobj"},
    },
    {
        "LEFT_ID": "as_object",
        "REL_OP": ">",
        "RIGHT_ID": "as_object_modifier",
        "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "prep"]}},
    }
    ]

    matcher.add("AS", [pattern])
    doc = nlp("my identity as a brown person is crucial to my opinion that dogs are extremely cute")
# tokenize sentence
# find index of pattern
# find token index of anchor word e.g. AS - what about "other X like me"
# what if there are other instances of AS
# token index -> object, modifiers, just get all children?

    matches = matcher(doc)

    match_id, token_ids = matches[0]
    for i in range(len(token_ids)):
        print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
    NP = []
    return NP

if __name__ == '__main__':
    identity_patterns = ["as a", "other(.*)like me", "since I'm a", "because I'm a", "as a person with", "I'm a person with", "as a person of", "as someone of", "I'm a person of", "I'm someone of", "my experience as a", "I work as a", "my identity as a", "my time as a", "my work as a", "as a(.*)citizen", "as an(.*)citizen", "as a(.*)user", "as an(.*)user"]
    # if pattern ends with " a" repeat with "n" added 
    # open file of tweets
    # iterate through tweets
    # for each tweet:
    found_patterns = search_for_patterns(tweet_body, identity_patterns)
    if len(found_patterns) != 0:
        NP = dependency_parsing(found_patterns)

    print(found_patterns, NP)




