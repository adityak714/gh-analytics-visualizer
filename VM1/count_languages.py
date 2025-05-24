from collections import Counter


from collections import Counter

def num_of_languages(repo_list):
    languages = [repo.get("language") for repo in repo_list if repo.get("language")]
    return Counter(languages)
