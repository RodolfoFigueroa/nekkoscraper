import scraper

url = "https://kitsunekko.net/dirlist.php?dir=subtitles"
root = "./zips/"

if __name__ == "__main__":
        # if "font".casefold() not in f[1].casefold() and "fonts".casefold() not in f[1].casefold():
        #     directory = root + f[0]
        #     if not os.path.isdir(directory):
        #         os.mkdir(directory)
        #     wget.download(f[1], directory)
    scraper.list_files(url, path=root+"filelist.txt", max_urls=5)