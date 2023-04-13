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
    authors_list = []
    authors_html = soup.find_all('small', class_='author')
    for author in authors_html:
        authors_list.append(author.text)
    print(authors_list)
    quotes_list = []
    quotes = soup.find_all('span', class_='text')
    for q in quotes:
        quotes_list.append(q.text)
    print(quotes_list)
    tags_list = []
    tags = soup.find_all('div', class_='tags')
    for t in tags:
        t_new = t.text.removeprefix('\n            Tags:\n            ').removesuffix('\n').strip().split('\n')
        tags_list.extend(t_new)
    print(tags_list)


    list_author_url = soup.find_all('about')
    print(list_author_url)
    for l in list_author_url:
        l = url + l



def main():
    for i in range(1,11):
        new_url = base_url + "/page/" + str(i)
        get_info(new_url)


if __name__== "__main__":
    main()
