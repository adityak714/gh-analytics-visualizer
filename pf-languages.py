import json
from collections import Counter

"""
This Pulsar function is for finding the top 10 programming languages based on the number of projects developed in them.
It comes as a middleman, filtering out just the metadata it is made for (Programming Language used).

This subscribes to "repos-raw" (where GitHub API responses are fetched), and emits at a * new * topic "top-10-programming-languages", 
that the end consumer will subscribe to.
"""

"""
A consumer currently is subscribing to:
    'persistent://public/default/repos-raw',
    to which the producer sends the whole project info as JSON.

    "... for repos in repo: ..." (probably one by one?) 
"""

# function name: process, with parameter 'input' based on the signature of Pulsar Function
def process(input): # the input is in the form of JSON, of metadata of one or multiple projects
    list_of_languages = []

    for i in range(100):
        items = input["items"][i]
        language = items.get("language")
        if (language == None):
            None
        else:
            list_of_languages.append(language)
    
    counted_list_of_languages = Counter(list_of_languages)
    
    print(type(counted_list_of_languages))
    return counted_list_of_languages