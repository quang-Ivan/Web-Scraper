from urllib import parse
from bs4 import BeautifulSoup
import requests
import re
import string
import os


def pre_process(url, typ, page=1):
    url = f"{url}{page}"
    r = requests.get(url)
    if r:
        soup = BeautifulSoup(r.content, "lxml")
        articles = soup.find_all("article")
        url_ = []
        for article in articles:
            type_ = article.find("span", {'data-test': "article.type"})
            if type_.text.strip().upper() == typ.upper():
                url_.append(article.find("a", {"data-track-action": "view article"}).get("href"))
        full_url = [parse.urljoin(url, i) for i in url_]
        try:
            os.mkdir(f"page_{page}")
        except FileExistsError:
            pass

        return [full_url, f"page_{page}"]
    else:
        print(f"error code {r.status_code} with {url}")
        return None


def scrap_and_save(url, path=os.getcwd()):
    r = requests.get(url)
    if r:
        soup = BeautifulSoup(r.content, "lxml")
        title = soup.find("h1",
                          {"class": "c-article-magazine-title"}).text  # find title with h1 class,usually the true title

        paras = soup.find("body").find('div', class_='c-article-body main-content')  # find paragraph in body
        # in div with class of main content

        title = re.sub(rf'[{string.punctuation}]', "", title)  # delete punctuation
        title = re.sub(rf'\s', "_", title)
        f_path = os.path.join(path, f"{title}.txt")
        with open(f_path, "w", encoding="utf-8") as f:
            f.writelines(paras.text.strip())
        return f"{title}.txt"
    else:
        print(f"error code {r.status_code} with {url}")
        return None


def main():
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="
    page = int(input("page"))
    typ = input("type")
    for i in range(page):
        page_ = i + 1
        full_url = pre_process(url, typ, page_)[0]
        path = pre_process(url, typ, page_)[1]
        for j in full_url:
            scrap_and_save(j, path)
        print(f"page {page_} saved")


if __name__ == "__main__":
    main()
