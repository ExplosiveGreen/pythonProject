from random import randint
import json
import requests_cache
import os


# a class of a tv show series.
# created in order for the random not give me a 2 season of tv show before I watch the first season
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


# getting my anime list from the website MyAnimeList
# if it can't reach the website it uses the text file
# hard copy of the anime list from the last time it reached the website
def get_data():
    text_path = os.path.dirname(__file__) + "\\resource\\anime_list\\anime_list.txt"
    cache_path = os.path.dirname(__file__) + "\\resource\\anime_list\\cache"
    requests = requests_cache.CachedSession(cache_path, backend='sqlite', expire_after=86400)
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
        f = open(text_path, "w")
        f.write(json.dumps(data))
        f.close()
        return data

    except requests.ConnectionError:
        f = open(text_path, "r")
        data = json.loads(f.read())
        f.close()
        return data


# cleaning up the anime list raw data and shuffle the list
# flag if True the function will print all shuffled list
def anime_list():
    anime = list()
    data = get_data()
    pos = "ExplosiveGreen"
    for r in data:
        if r["anime_media_type_string"] == u'OVA' or r["anime_media_type_string"] == u'Movie' or r["anime_media_type_string"] == u'Special':
            continue
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

    return {'result': shuffle(anime)}


def modText(text, word_count):
    text = text.split(" ")
    add = 0
    for i in range((len(text) - 1) // word_count):
        text.insert((i + 1) * word_count + add, "\n")
        add += 1
    return " ".join(text)


# create a gui representation for the shuffle anime list
def gui_anime_list():
    import tkinter as tk
    from tkinter.font import Font
    import pyperclip
    window = tk.Tk()
    window.geometry("720x720")
    color = '#ffffff'
    color_dark = '#646464'
    bg = '#3c193c'
    width_ratio = 750 / 40
    height_ratio = 750 / 19
    font = Font(size=20)
    window.update()
    width = window.winfo_width()
    height = window.winfo_height()
    index = 0
    word_count = 4
    window.configure(bg=bg)
    anime = anime_list()['result']
    anime_title = tk.Label(text=modText(str(anime[index]), word_count), bg=bg, font=font, fg=color,
                           width=int(width / width_ratio), height=int(height / height_ratio / 2))
    anime_title.pack()

    def Next():
        nonlocal index
        index += 1
        if index >= len(anime):
            window.destroy()
        else:
            anime_title.config(text=modText(str(anime[index]), word_count))

    def List():
        str1 = ""
        for i in range(index, len(anime)):
            str1 += u"{}:{}\n".format(i, anime[i])
        pyperclip.copy(str1)
        # print(str1)

    def Quit():
        window.destroy()

    def copy():
        pyperclip.copy(u'{}'.format(anime[index]))

    tk.Button(window, text="next", command=Next, font=font, bg=color_dark, fg=color, width=width).pack()
    tk.Button(window, text="list", command=List, font=font, bg=color_dark, fg=color, width=width).pack()
    tk.Button(window, text="copy", command=copy, font=font, bg=color_dark, fg=color, width=width).pack()
    tk.Button(window, text="quit", command=Quit, font=font, bg=color_dark, fg=color, width=width).pack()
    window.mainloop()


# shuffle the list
def shuffle(anime):
    shuffle_anime = list()
    while len(anime) > 0:
        index = randint(0, len(anime) - 1)
        anime1, flag = anime[index].__str__()
        if not flag:
            del anime[index]
        else:
            shuffle_anime.append(anime1)
    return shuffle_anime


if __name__ == '__main__':
    gui_anime_list()
