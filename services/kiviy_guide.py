import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class GuideApp(App):
    def build(self):
        return Builder.load_file("resource/kiviy_guide/guide.kv")


if __name__ == "__main__":
    GuideApp().run()
