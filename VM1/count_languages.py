from collections import Counter

#Returns a list of tuples where we count the occurance of each language
#Takes a list of repositories
def num_of_languages(repo_list):
    languages = [repo.get("language") for repo in repo_list if repo.get("language")]
    return Counter(languages)
