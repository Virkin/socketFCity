from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot
from random import randint
from time import strftime, gmtime

class GraphScreen(Screen):
    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.layoutgraph = RelativeLayout()
        self.layoutgraph.add_widget(self.build())
        self.gotomain = Button(text="Back to main screen", size=(250, 30), size_hint=(None, None), on_release=self.switchtomain)
        self.layoutgraph.add_widget(self.gotomain)
        self.add_widget(self.layoutgraph)

    def switchtomain(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = "main"

    def build(self):
        self.graph = Graph(
            xlabel='Nombre de secondes écoulées',
            ylabel='Vitesse km/h',
            x_ticks_minor=1,
            x_ticks_major=10,
            y_ticks_minor=1,
            y_ticks_major=5,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=False,
            y_grid=False,
            xmin=0,
            xmax=1,
            ymin=0,
            ymax=1)
        self.index = 0
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.plot.points = []
        Clock.schedule_interval(self.update_points, 1)
        return self.graph

    def update_points(self, *args):
        self.plot.points.append(tuple((self.index, self.number())))
        self.graph.xmax += 1
        if len(self.plot.points) > 60:
            self.graph.xmin += 1
            self.plot.points.pop(-len(self.plot.points))
        self.index += 1
        self.graph.xlabel = "Nombre de secondes écoulées => {}".format(strftime("%Hh%Mm%Ss", gmtime(self.index)))

    def number(self):
        number = randint(0, 50)
        if number > self.graph.ymax:
            self.graph.ymax = number
        return number

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layoutmain = BoxLayout(orientation="horizontal")
        self.gotograph = Button(text="Graph", on_release=self.switchtograph)
        self.layoutmain.add_widget(self.gotograph)
        self.add_widget(self.layoutmain)

    def switchtograph(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "graph"


class NavigationApp(App):
    def build(self):
        sm = ScreenManager()
        mainscreen = MainScreen(name="main")
        graphscreen = GraphScreen(name="graph")
        sm.add_widget(mainscreen)
        sm.add_widget(graphscreen)
        return sm

NavigationApp().run()
