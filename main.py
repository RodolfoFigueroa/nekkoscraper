import requests, zipfile, io, os, wget
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs, quote_plus

internal_urls = set()
url = "https://kitsunekko.net/dirlist.php?dir=subtitles"
# url = "https://scrapethissite.com/pages"


def is_valid(u):
    parsed = urlparse(u)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_links(u):
    urls = set()
    parsed_url = urlparse(u)
    top_domain = parsed_url.scheme + "://" + parsed_url.netloc + "/"
    soup = BeautifulSoup(requests.get(u).content, "html.parser")
    for t in soup.findAll("a"):
        href = t.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(u, href)
        parsed_href = urlparse(href)
        qs = parse_qs(parsed_href.query)
        if len(qs)==1:
            ap = "?dir=" + quote_plus(qs['dir'][0], safe='/')
            if ap[-1] != "/":
                ap = ""
        else:
            ap = ""
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + ap
        if top_domain != href and is_valid(href) and href not in internal_urls and top_domain in href:
            print("INTERNAL", href)
            urls.add(href)
            internal_urls.add(href)
    return urls


total_urls_visited = 0
max_urls = 5
extensions = {"ass", "srt", "zip", "rar", "7z", "ssa"}


def crawl(url):
    global total_urls_visited
    total_urls_visited += 1
    print(total_urls_visited)
    qs = parse_qs(urlparse(url).query)
    if qs:
        title = qs['dir'][0].split("subtitles")[1][1:-1]
        print(title)
    links = get_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        ext = link.rsplit(".", 1)[-1].casefold()
        if ext in extensions:
            print(f"FILE: {link}")
            filelist.append([title,link])
        else:
            crawl(link)


if __name__ == "__main__":
    filelist = []
    root = "C:\\Users\\Rodolfo\\Documents\\NLP\\anisub\\zips\\"
    crawl(url)
    for f in filelist:
        if "font".casefold() not in f[1].casefold() and "fonts".casefold() not in f[1].casefold():
            dir = root + f[0]
            if not os.path.isdir(dir):
                os.mkdir(dir)
            wget.download(f[1], dir)