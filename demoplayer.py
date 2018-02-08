"""v0.1 Licenced under MIT License"""
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from pathlib import Path
import os
import win32com.client
import time
import keyboard
import sys

class DemoListButton(ListItemButton):
    pass

class SettingsPopup(Popup):
    reflex_path_text = ObjectProperty()
    demo_path_text = ObjectProperty()

    def update_settings(self):
        r = open("./reflex.cfg", "w+")
        r.write(self.reflex_path_text.text)
        r.close()
        d = open("./demos.cfg", "w+")
        d.write(self.demo_path_text.text)
        d.close()

    def check_demos(self):
        return open("./demos.cfg").read()

    def check_reflex(self):
        return open("./reflex.cfg").read()

class DemoFinder(BoxLayout):
    reflex_path_text = ObjectProperty()
    demo_list = ObjectProperty()
    last_path_bot = ObjectProperty()
    last_path = ""

    def delete_demos(self):
        if self.demo_list.adapter.selection:
            for any in self.demo_list.adapter.selection:
                self.demo_list.adapter.data.remove(any.text)

    def clear_demo_list(self):
        self.last_path = ""
        self.last_path_bot = ""
        self.demo_list.adapter.data = []

    def populate_demo_list(self):
        demo_cfg_path = open("demos.cfg").read()
        self.last_path_bot = demo_cfg_path
        if not demo_cfg_path:
            SettingsPopup().open()
        elif demo_cfg_path:
            try:
                for demo in os.listdir(demo_cfg_path):
                    if demo not in self.demo_list.adapter.data:
                        self.demo_list.adapter.data.extend([demo])
                self.demo_list.adapter.data = sorted(self.demo_list.adapter.data)
            except FileNotFoundError:
                pass
            if self.demo_list.adapter.selection:
                try:
                    concat = os.path.join(demo_cfg_path, self.demo_list.adapter.selection[0].text)

                    if self.last_path:
                        deeper = os.path.join(self.last_path, self.demo_list.adapter.selection[0].text)
                        for deep_demo in os.listdir(deeper):
                            if deep_demo not in self.demo_list.adapter.data:
                                self.demo_list.adapter.data.extend([deep_demo])
                    else:
                        for deep_demo in os.listdir(concat):
                            if deep_demo not in self.demo_list.adapter.data:
                                self.demo_list.adapter.data.extend([deep_demo])
                    self.last_path = concat
                    self.last_path_bot = concat
                    self.demo_list.adapter.data = sorted(self.demo_list.adapter.data)

                except (NotADirectoryError, FileNotFoundError) as e:
                    pass
        else:
            pass


    def play_demo(self):
        if len(self.demo_list.adapter.selection) == 1:
            selection = self.demo_list.adapter.selection[0].text
            if selection[-4:] == ".rep":
                shell = win32com.client.Dispatch("WScript.Shell")
                try:
                    cwd = os.getcwd()
                    path = open("reflex.cfg", "r").read()
                    os.chdir(path)
                    shell.Run(r"reflex.exe")
                    shell.AppActivate("reflex.exe")
                    os.chdir(cwd)
                    time.sleep(8)
                    keyboard.press_and_release("`")
                    time.sleep(1)
                    keyboard.write("play " + str(selection[:-4]))
                    time.sleep(1)
                    keyboard.press_and_release("enter")
                    time.sleep(1)
                    keyboard.press_and_release("`")
                    time.sleep(5)
                    return

                except (FileNotFoundError, OSError) as e:
                    SettingsPopup().open()

            else:
                pass

    def open_popup(self):
        SettingsPopup().open()



class DemoFinderApp(App):
    def build(self):
        return DemoFinder()

if __name__ == '__main__':
    demoApp = DemoFinderApp()
    demoApp.run()
