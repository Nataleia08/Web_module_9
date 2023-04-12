import requests
from bs4 import BeautifulSoup

base_url = 'http://quotes.toscrape.com/'


def list_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    authors = soup.find_all('small', class_='author')
    print(authors)
    list_author_url = soup.find_all('a href', class_='author')
    print(list_author_url)
    for l in list_author_url:
        l = url + l

    quotes = soup.find_all('span', class_='text')
    print(quotes)
    tags = soup.find_all('div', class_='tags')



def author_list(url_list):
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')




if __name__== "__main__":
    list_url(base_url)



# for i in range(0, len(quotes)):
#     print(quotes[i].text)
#     print('--' + authors[i].text)
#     tagsforquote = tags[i].find_all('a', class_='tag')
#     for tagforquote in tagsforquote:
#         print(tagforquote.text)
#     break