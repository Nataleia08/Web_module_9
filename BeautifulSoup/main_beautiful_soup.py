import requests
from bs4 import BeautifulSoup
import json

base_url = 'http://quotes.toscrape.com/'


def save_info(name_file, dump_info):
    with open(name_file, "a", encoding='utf-8') as fh:
        json.dump(dump_info, fh)

def get_info_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    authors_html = soup.find_all('small', class_='author')
    quotes_html = soup.find_all('span', class_='text')
    tags_html = soup.find_all('div', class_='tags')
    tags_all_list = []
    quotes_list = []
    for i in range(len(authors_html)):
        quotes = {}
        quotes["author"] = authors_html[i].text
        quotes["quote"] = quotes_html[i].text
        quotes["tags"] = tags_html[i].text.removeprefix('\n            Tags:\n            ').removesuffix('\n').strip().split('\n')
        quotes_list.append(quotes)
        tags_all_list.extend(quotes["tags"])
    save_info("quotes.json", quotes_list)

    return set(tags_all_list)

def get_info_author(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    authors_url = soup.find_all('a', href_='author')
    print(authors_url)




def main():
    tags_list = get_info_quotes(base_url)
    for i in range(2,11):
        new_url = base_url + "/page/" + str(i)
        tags_list.union(get_info_quotes(new_url))
    print(tags_list)
    for t in tags_list:
        new_url = base_url + "/tag/" + t
        get_info_quotes(new_url)
    get_info_author(base_url)


if __name__== "__main__":
    main()
