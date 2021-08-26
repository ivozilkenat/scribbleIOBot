from webdriverLib import *
from GoogleImageSearch import *
from PIL import Image
import pyautogui as pag
import pytesseract, os, cv2, math, colorsys
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\hoisc\AppData\Local\Tesseract-OCR\tesseract.exe"

class Bot():
    def __init__(self, player, url, speed = 1000):
        self.chromeOptions = Options()
        self.chromeOptions.add_argument('--disable-notfications')
        self.chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Chrome(options=self.chromeOptions)
        self.element = Element(self, waitTime=10)
        self.player = player
        self.wanna_draw = 1
        self.set_window()
        self.states = ["|", "/", "-", "\\"]
        self.status = self.states[0]
        self.color_pallet = None
        self.current_color = Color((0, 0), (255, 255, 255))
        self.speed = speed
        pag.PAUSE = 1/self.speed

        self.enter_game(url)
        print("[Srikkbl.io succesfully loaded]")
        self.join_lobby()
        print("[succesfully joined lobby]")

        print("""
Drücke eine Taste um den BOT zu aktivieren. 
Da man nicht feststellen kann, ob das Spiel bereits beginnt,
musst du den Bot manuell starten, sonst können Fehler auftreten.
                            """)
        input("'Beliebige Taste'")
        self.game_loop()
    def set_window(self):
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1920, 1080)
    def enter_game(self, url):
        self.gotoWebPage(url)
    def join_lobby(self):
        self.element.ByXpath('//*[@id="cmpwelcomebtnyes"]/a').click()
        self.element.ByXpath('//*[@id="inputName"]').send_keys(self.player)
        self.element.ByXpath('//*[@id="formLogin"]/button[1]').click()
    def gotoWebPage(self, url, trys = 50):
        c = 0
        while c < trys:
            time.sleep(0.2)
            self.browser.get(url)
            if self.browser.current_url == url:
                break
            elif c >= trys:
                raise RuntimeError("Given URL not accessible")
    def check_for_drawing(self):
        #Region ist nicht passend
        img = pag.screenshot(region=(720, 200, 480, 60))
        return pytesseract.image_to_string(img).strip()

    def delete_all_files_in(self, dir):
        [os.remove(os.path.join(dir, file)) for file in os.listdir(dir)]

    def create_color_pallet(self, position, rows, columns, color_size):
        colors = []
        print("[creating colorpallet]")
        for row in range(rows):
            for column in range(columns):
                pos = (int(position[0] + color_size/2 + color_size * column), int(position[1] + color_size/2 + color_size * row))
                pag.moveTo(pos)
                time.sleep(1)
                colors.append(Color(pos, pag.pixel(*pos)))
        print("[created colorpallet]")
        return colors

    def draw(self, word):
        brush_sizes, brush_size = [(3, (1040, 920)), (6, (1090, 920)), (15, (1140, 920)), (30, (1190, 920))], None
        print("Auflösungen:")
        for c, i in enumerate(brush_sizes):
            print(f"{c + 1}. - {i[0]}")
        while 1:
            i = int(input("Auflösung wählen: "))
            if i in range(1, len(brush_sizes)+1):
                brush_size = brush_sizes[i - 1][0]
                pag.click(brush_sizes[i - 1][1])
                break

        print("[Bild wird gesucht]")
        i = ImgSearch()
        i.search_for(word)
        print(f"[Bild von '{word}' erfolgreich runtergeladen]")

        field_size = field_w, field_h = 814, 610
        x_canvas, y_canvas, x_color, y_color = 488, 276, 574, 910
        rows, columns, color_size = 2, 11, 24
        if self.color_pallet == None:
            self.color_pallet = self.create_color_pallet((x_color, y_color), rows, columns, color_size)
        img = cv2.imread(os.path.join(ImgSearch.data_dir, f"{word}.jpg"))
        w, h = int(field_w / brush_size), int(field_h / brush_size)
        img = cv2.resize(img, (w, h))
        instruction_list = []
        print(f"[Auflösung: {w * h}px]")
        print("[Bildpunkte werden berechnet]")
        #Farbauswahl fehlerhaft
        for c1, row in enumerate(img):
            for c2, pixel in enumerate(row):
                total_pixels = c1 * w + c2
                if total_pixels % 1000 == 0:
                    print(f"[Fortschritt: {round((total_pixels*100)/(w*h), 1)}%]", end="\r")
                pos = (x_canvas + brush_size * c2, y_canvas + brush_size * c1)
                instruction_list.append((pos, self.nearest_color(Color(None,pixel).color)))
        instruction_list.sort(key=lambda x: sum(x[1].color))
        print("[Berechnung abgeschlossen]", end="\r")

        for i in instruction_list:
            if self.still_drawing():
                if self.current_color != i[1]:
                    self.current_color = self.color_pallet[self.color_pallet.index(i[1])]
                    pag.click(x=self.current_color.pos[0], y=self.current_color.pos[1])
                if self.current_color.color == (360, 100, 100): #HSV - Hue 360, Saturation 100, Value 100
                    continue
                else:
                    pag.click(x=i[0][0], y=i[0][1])

        #wenn zuvor beendet, dann abbrechen
        self.delete_all_files_in(ImgSearch.data_dir)
        print(f"['{word}' wurde vollständig gemalt]")

    def still_drawing(self):
        #Nicht implementiert
        #Wenn Runde zuende (Zeit, erraten, etc.) False returnen
        #1.check for open window
        return True

    def nearest_color(self, color):
        #Farben immer noch fehlerhaft
        h1, s1, v1 = color
        h_factor, s_factor, v_factor = 5, 2.8, 2.2
        return sorted(self.color_pallet, key=lambda x: abs(h1-x.color[0]) * h_factor + abs(s1-x.color[1]) * s_factor + abs(v1-x.color[2]) * v_factor)[0]

    def load_icon(self):
        i = self.states.index(self.status)+1
        if i >= len(self.states):
            i = 0
        self.status = self.states[i]
        print(self.status, end="\r")

    def game_loop(self):
        while True:
            self.set_window()
            self.load_icon()
            word = self.check_for_drawing().strip().replace("\n", "")
            if word != '' and self.wanna_draw == 1:
                print("-------------------------------------------------------------")
                print(f"Möchtest du, dass das Programm '{word}' malt?")
                while 1:
                    i = input("(Y/N): ")
                    if i.capitalize() == "Y":
                        self.draw(word)
                        break
                    elif i.capitalize() == "N":
                        print(f"Möchtest du, dass das Programm ein custom Wort malt?")
                        i = input("('Word'/N): ")
                        if i.capitalize() != "N":
                            self.draw(i)
                        break
                self.wanna_draw = 0
            elif word == "" and self.wanna_draw == 0:
                self.wanna_draw = 1
            time.sleep(0.1)

class Color():
    rgb = "rgb"
    hsv = "hsv"
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.color_model = Color.rgb
        self.color = self.convert2hsv()
    def convert2hsv(self):
        if self.color_model != Color.hsv:
            self.color_model = Color.hsv
            h, s, v = colorsys.rgb_to_hsv(*[self.floatFromInt(i) for i in self.color])
            return self.intFromFloat(h, 360), self.intFromFloat(s, 100), self.intFromFloat(v, 100)
    #def convert2rgb(self):
    #   if self.color_model != Color.rgb:
    #        self.color_model = Color.rgb
    @staticmethod
    def floatFromInt(num, max=255):
        return num/max
    @staticmethod
    def intFromFloat(num, max):
        return round(num*max)