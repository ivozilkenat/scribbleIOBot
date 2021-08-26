from webdriverLib import *
import urllib.request, os

class ImgSearch():
    data_dir = "data"
    def __init__(self):
        self.chromeOptions = Options()
        self.chromeOptions.add_argument('--disable-notfications')
        self.chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Chrome(options=self.chromeOptions)
        self.element = Element(self, waitTime=10)
    def search_for(self, word):
        self.browser.get(f'https://www.google.com/search?q={word}&tbm=isch')
        urllib.request.urlretrieve(self.element.ByTagName("img").element.get_attribute("src"), os.path.join(ImgSearch.data_dir, f"{word}.jpg"))
        self.browser.close()

#zufällig ein bild auswählen