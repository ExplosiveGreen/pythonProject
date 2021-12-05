import random as rnd
import json
import requests

#a class of a tv show series.
#created in order for the random not give me a 2 season of tv show befor i watch the first season
class Series:
    def __init__(self, name):
        self.name = name
        self.index = 0
        self.series_list = list()
        self.series_list.append(name)

    def add(self, anime):
        self.series_list.append(anime)

    def __str__(self):
        flag = True
        if len(self.series_list) > self.index:
            ans = self.series_list[self.index]
        else:
            flag = False
            ans = "no more"
        self.index += 1
        return ans, flag

#geting my anime list from the website myanimelist
#if it can reach the website it use the text file
#hard copy of the anime list from the last time it manage to reach the website
def get_data():
    try:
        offset = 0
        html = requests.get("https://myanimelist.net/animelist/ExplosiveGreen/load.json?status=2")
        temp = json.loads(html.text)
        data = list()
        while len(temp) == 300:
            offset += 300
            data.extend(temp)
            html = requests.get(
                "https://myanimelist.net/animelist/ExplosiveGreen/load.json?offset={}&status=2".format(offset))
            temp = json.loads(html.text)
        if temp:
            data.extend(temp)
        f = open("../resource/anime_list/anime_list.txt", "w")
        f.write(json.dumps(data))
        f.close()
        return data

    except requests.ConnectionError:
        f = open("../resource/anime_list/anime_list.txt", "r")
        data = json.loads(f.read())
        f.close()
        return data

#cleaning up the anime list raw data and shuffle the list
#flag if True the function will print the entier shuffled list
def anime_list(flag=True):
    anime = list()
    data = get_data()
    pos = "ExplosiveGreen"
    for r in data:
        if r["anime_media_type_string"] != u'OVA' and r["anime_media_type_string"] != u'Movie' and \
                r["anime_media_type_string"] != u'Special':
            if pos in str(r["anime_title"]):
                if r["anime_title_eng"]:
                    anime[len(anime) - 1].add(r["anime_title_eng"])
                else:
                    anime[len(anime) - 1].add(r["anime_title"])
            else:
                pos = str(r["anime_title"])
                if r["anime_title_eng"]:
                    anime.append(Series(r["anime_title_eng"]))
                else:
                    anime.append(Series(r["anime_title"]))

    shuffle1 = shuffle(anime)
    if flag:
        count = 0
        for anime in shuffle1:
            count += 1
            print (u"{}: {}".format(count, anime))
    else:
        return shuffle1

#create a gui representation for the shuffle anime list
def gui_anime_list():
    mouse = []
    import pygame
    import pyperclip
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    width = screen.get_width()
    height = screen.get_height()
    small_font = pygame.font.SysFont('Corbel', 35)
    buttons = list()
    buttons.append(small_font.render('next', True, color))
    buttons.append(small_font.render('list', True, color))
    buttons.append(small_font.render('copy', True, color))
    buttons.append(small_font.render('quit', True, color))
    index = 0
    word_count = 4
    anime = anime_list(False)
    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if height / 2 <= mouse[1] <= height / 2 + 40:
                    if index < len(anime):
                        index += 1
                    else:
                        pygame.quit()
                if height / 2 + 41 <= mouse[1] <= height / 2 + 81:
                    for i in range(index, len(anime)):
                        print(u"{}:{}".format(i, anime[i]))
                if height / 2 + 82 <= mouse[1] <= height / 2 + 122:
                    pyperclip.copy(u'{}'.format(anime[index]))
                if height / 2 + 123 <= mouse[1] <= height / 2 + 163:
                    pygame.quit()
        screen.fill((60, 25, 60))
        mouse = pygame.mouse.get_pos()
        for key, j in enumerate(range(0, 124, 41)):
            if height / 2 + j <= mouse[1] <= height / 2 + j + 40:
                pygame.draw.rect(screen, color_light, [0, height / 2 + j, 720, 40])
            else:
                pygame.draw.rect(screen, color_dark, [0, height / 2 + j, 720, 40])
            screen.blit(buttons[key], ((width - buttons[key].get_width()) / 2, height / 2 + j))
        anime_title = str(anime[index]).split(" ")
        for pos in range(len(anime_title)//word_count + (0 if len(anime_title) % word_count == 0 else 1)):
            sentence = ""
            for pos2 in range(word_count):
                if pos*word_count + pos2 < len(anime_title):
                    sentence += anime_title[pos*word_count + pos2]+" "
            text = small_font.render(sentence, True, color)
            screen.blit(text, ((width - text.get_width()) / 2, height / 4 + pos*small_font.get_height()))
        pygame.display.update()

#shuffle the list
def shuffle(anime):
    rnd.seed()
    shuffle_anime = list()
    while len(anime) > 0:
        index = rnd.randint(0, len(anime) - 1)
        anime1, flag = anime[index].__str__()
        if not flag:
            del anime[index]
        else:
            shuffle_anime.append(anime1)
    return shuffle_anime


if __name__ == '__main__':
    gui_anime_list()
