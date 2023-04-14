import requests
from bs4 import BeautifulSoup
import json

base_url = 'http://quotes.toscrape.com/'


def save_info(name_file, dump_info):
    with open(name_file, "a", encoding='utf-8') as fh:
        json.dump(dump_info, fh)
        json.dump("\n",fh)

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

def get_url_author(url):
    response = requests.get(url)
    authors_url_list = []
    soup = BeautifulSoup(response.text, 'lxml')
    for a in soup.find_all('a'):
        authors_url = a.attrs.get("href")
        if "/author/" in authors_url:
            authors_url_list.append(authors_url)
    return authors_url_list


def get_info_author(url) -> dict:
    new_author = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    new_author["fullname"] = soup.find_all('h3', class_='author-title')[0].text.strip().removesuffix("\n")
    new_author["born_date"] = soup.find_all('span', class_='author-born-date')[0].text
    new_author["born_location"] = soup.find_all('span', class_='author-born-location')[0].text
    new_author["description"] = soup.find_all('div', class_='author-description')[0].text.removeprefix('\n').strip()
    # print(new_author)
    return new_author


    #save_info("author.json", )


def main():
    author_url_list = []
    author_list = []
    tags_list = get_info_quotes(base_url)
    author_url_list.extend(get_url_author(base_url))
    for i in range(2,11):
        new_url = base_url + "/page/" + str(i)
        tags_list.union(get_info_quotes(new_url))
        author_url_list.extend(get_url_author(new_url))
    print(tags_list)
    for t in tags_list:
        new_url = base_url + "/tag/" + t
        get_info_quotes(new_url)
    for u in author_url_list:
        k = get_info_author(base_url + u)
        in_list = False
        for a in author_list:
            if a['fullname'] == k['fullname']:
                in_list = True
        if not in_list:
            author_list.append(k)
    print(author_list)
    # print(author_list)
    save_info("author.json", author_list)




if __name__== "__main__":
    main()
