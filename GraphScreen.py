from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot
from time import strftime, gmtime


class GraphScreen(Screen):
    def __init__(self, q, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.layoutgraph = RelativeLayout()
        self.layoutgraph.add_widget(self.build())
        self.gotomain = Button(text="Retour", size=(200, 35), size_hint=(None, None), on_release=self.switchtomain)
        self.labelswitch = Label(text="Dernière minute", size_hint=(None, None), pos_hint={'center_x': .82, 'center_y': .04})
        self.switch = Switch(active=False, size=(100, 35), size_hint=(None, None), pos_hint={'center_x': .94, 'center_y': .04})
        self.layoutgraph.add_widget(self.gotomain)
        self.layoutgraph.add_widget(self.labelswitch)
        self.layoutgraph.add_widget(self.switch)
        self.add_widget(self.layoutgraph)
        self.q = q

    def switchtomain(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = "main"

    def build(self):
        self.graph = Graph(
            xlabel='Secondes écoulées',
            ylabel='Puissance (W)',
            x_ticks_minor=1,
            x_ticks_major=1,
            y_ticks_minor=1,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=10,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=1,
            ymin=0,
            ymax=1)
        self.index = 0
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.plot.points = []
        self.offset = 1
        Clock.schedule_interval(self.update_points, 1)
        return self.graph

    def update_points(self, *args):
        if not self.q.empty():
            if len(self.plot.points) > 1:
                self.graph.xmax += 1

            self.plot.points.append(tuple((self.index, self.number())))

            if self.switch.active:
                if len(self.plot.points) > 60:
                    self.graph.xmin = self.graph.xmax - 60

                    i = len(self.plot.points) - 60

                    lastminMin = self.plot.points[i-1]
                    lastminMax = self.plot.points[i-1]
                
                    for i in range(i,i+60) :
                        if self.plot.points[i] < lastminMin :
                            lastminMin = self.plot.points[i]
                        elif self.plot.points[i] > lastminMax :
                            lastminMax = self.plot.points[i]

                    self.graph.ymin = lastminMin - self.offset
                    self.graph.ymax = lastminMax + self.offset
            else:
                self.graph.xmin = 0
                self.graph.ymin = self.min
                self.graph.ymax = self.max

            #if len(self.plot.points) > 60:
            #    self.graph.xmin += 1
            #    self.plot.points.pop(-len(self.plot.points))

            self.graph.y_ticks_major = (self.graph.ymax - self.graph.ymin) / 10
            self.graph.x_ticks_major = (self.graph.xmax - self.graph.xmin) / 10

            self.graph.xlabel = "Secondes écoulées => {}".format(strftime("%Hh%Mm%Ss", gmtime(self.index)))
            self.index += 1

    def number(self):
        number = self.q.get()

        if number > self.graph.ymax:
            self.max = number + self.offset
        elif number < self.graph.ymin or self.graph.ymin == 0:
            self.min = number - self.offset

        return number
