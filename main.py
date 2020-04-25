import os
import requests
import wget

url = "https://kitsunekko.net/dirlist.php?dir=subtitles"
root = "./zips/"

if __name__ == "__main__":
    filelist = open(root+"temp.txt", 'r', encoding='utf-8')
    for strline in filelist:
        try:
            line = eval(strline)
            print("OPENING:", line)
            directory = root + line[0]
            if not os.path.isdir(directory):
                os.mkdir(directory)
            for file in line[1:]:
                req = requests.head(file)
                if int(req.headers.get("Content-Length")) < 20000000 and "font".casefold() not in file.casefold():
                    print("DOWNLOADING", file)
                    wget.download(file, directory)
        except:
            pass