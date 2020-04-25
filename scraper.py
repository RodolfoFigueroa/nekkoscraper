import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs, quote_plus


internal_urls = set()


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
        if "dir" in qs.keys():
            ap = "?dir=" + quote_plus(qs['dir'][0], safe='/')
            if ap[-1] != "/": #workaround to ignore broken href tags in html
                ap = ""
        else:
            ap = ""
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + ap
        if top_domain != href and is_valid(href) and href not in internal_urls and top_domain in href:
            urls.add(href)
            internal_urls.add(href)
    return urls


total_urls_visited = 0
exclude = {".php"}
filelist = []


def crawl(u, max_urls):
    print("CHECKING", u)
    global total_urls_visited
    if 0 <= max_urls <= total_urls_visited:
        return
    total_urls_visited += 1
    print(total_urls_visited)
    qs = parse_qs(urlparse(u).query)
    title = "$$"
    if qs:
        title = qs['dir'][0].split("subtitles")[1][1:-1]
    out = [title]
    links = get_links(u)
    for link in links:
        ext = os.path.splitext(link)[1].casefold()
        if ext != "":
            if ext not in exclude:
                print("FILE: ", link)
                out.append(link)
        else:
            crawl(link, max_urls)
    if len(out) > 1:
        filelist.append(out)
    return


def list_files(u, path="filelist.txt", max_urls=-1):
    crawl(u, max_urls)
    global filelist
    with open(path, 'w', encoding='utf-8') as f:
        for item in filelist:
            f.write("%s\n" % item)
    return