from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from queue import Queue
from MainScreen import MainScreen
from GraphScreen import GraphScreen


class NavigationApp(App):
    def build(self):
        q=Queue()
        sm = ScreenManager()
        mainscreen = MainScreen(name="main", q=q)
        graphscreen = GraphScreen(name="graph", q=q)
        sm.add_widget(mainscreen)
        sm.add_widget(graphscreen)
        return sm

NavigationApp().run()
