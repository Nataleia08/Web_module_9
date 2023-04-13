import requests
from bs4 import BeautifulSoup
import json

base_url = 'http://quotes.toscrape.com/'


def save_info(name_file, dump_info):
    with open(name_file, "w", encoding='utf-8') as fh:
        json.dump(dump_info, fh)

def get_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    authors_html = soup.find_all('small', class_='author')
    quotes_html = soup.find_all('span', class_='text')
    tags_html = soup.find_all('div', class_='tags')
    tags_all_list = []
    for i in range(len(authors_html)):
        quotes_list = {}
        quotes_list["author"] = authors_html[i].text
        quotes_list["author"] = quotes_html[i].text
        quotes_list["tags"] = tags_html[i].text.removeprefix('\n            Tags:\n            ').removesuffix('\n').strip().split('\n')
        save_info("quotes.json", quotes_list)
        tags_all_list.extend(quotes_list["tags"])

    return set(tags_all_list)


    list_author_url = soup.find_all('about')
    print(list_author_url)
    for l in list_author_url:
        l = url + l



def main():
    tags_list = get_info(base_url)
    for i in range(2,11):
        new_url = base_url + "/page/" + str(i)
        tags_list.union(get_info(new_url))
    print(tags_list)
    for t in tags_list:
        new_url = base_url + "/tag/" + t
        get_info(new_url)


if __name__== "__main__":
    main()
