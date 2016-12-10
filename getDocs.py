import re
import urllib.request as ul
import os


class Page:
    url = html = "none"

    def __init__(self, url):
        self.url = url
        print("Start task:", self.url)
        self.startDownload()

    def startDownload(self):
        src = getSavePath(self.url)
        
        if os.path.isfile(src):
            file = open(src, "r", encoding="utf-8")
            self.html = file.read()
            file.close()
            print("    Read from local:",src)
        else:
            self.html = ul.urlopen(self.url).read().decode("utf-8")

            print("    Saved in:", src)

            if not os.path.isdir(clearDir(src)):
                os.makedirs(clearDir(src))

            file = open(src, "w", encoding="utf-8")
            file.write(self.html)
            file.close()

        self.getChild()

    def getChild(self):
        childList = re.findall(r"""<td class="name-cell">\s+?<a href="(.+?)"><p>(.+?)</p></a>\s+?</td>""", self.html)
        for each in childList:
            print("    Ready to start:",each)
            Page(clearDir(self.url) + each[0])


def getSavePath(url):
    return re.sub(r"^.+?/BlueprintAPI", os.getcwd(), url).replace("/","\\")


def clearDir(url):
    return url.replace("index.html", "")#.replace("/","\\")


url = "https://docs-origin.unrealengine.com/latest/INT/BlueprintAPI/index.html"
Page(url)
print("=====Finish=====")
