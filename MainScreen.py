from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.garden.mapview import MapView, MapMarker
from random import randint, uniform
from time import strftime
from evdev import InputDevice, categorize, ecodes, list_devices
from re import match
from datetime import datetime
from clientClass import ClientSocket
from mysql.connector import connect
from math import sin
from threading import Thread
from queue import Queue
from socket import gethostbyname, create_connection


class MainScreen(Screen):
    def __init__(self, q, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layoutmain = RelativeLayout()
        self.layoutmain.add_widget(self.build())
        self.on_start()
        self.add_widget(self.layoutmain)
        self.q = q

    def switchtograph(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "graph"

    def build(self):
        # Layout
        self.layout = BoxLayout(orientation="horizontal")
        self.toolbar = BoxLayout(orientation="vertical")
        self.toolbarlogograph = BoxLayout(orientation="horizontal")
        self.toolbarpuissance = BoxLayout(orientation="horizontal")
        self.toolbarvitesse = BoxLayout(orientation="horizontal")
        self.toolbaracceleration = BoxLayout(orientation="horizontal")
        self.toolbareclairement = BoxLayout(orientation="horizontal")
        self.maplayout = RelativeLayout()
        with self.toolbar.canvas.before:
            Color(1, 1, 1, .5)
            self.rect = Rectangle(size=self.toolbar.size, pos=self.toolbar.pos, source="fcity.jpg")
        self.toolbar.bind(pos=self.update_rect, size=self.update_rect)

        # Map
        self.map = MapView(zoom=16, lon=-4.5047, lat=48.3878, map_source="osm-fr")
        self.home = MapMarker(lon=-4.5047, lat=48.3878)
        self.map.add_marker(self.home)

        # Label
        self.titre = Label(text="[b]GPS FCity[/b] {}".format(datetime.now().strftime("%d/%m/%y %H:%M")), font_size="30sp", markup=True)
        self.logo = Image(source="ISEN-Brest_horizontal.jpg")
        self.wifi = Label(font_size="30sp", markup=True)
        self.graphpuissance = Button(text="Graphique", font_size="20sp", markup=True, on_release=self.switchtograph)
        self.labelpuissance = Label(text="[b]Puissance :[/b]", font_size="30sp", markup=True, halign="right", valign="middle")
        self.labelpuissance.bind(size=self.labelpuissance.setter('text_size'))
        self.puissance = Label(font_size="30sp", size_hint=(.8, 1), markup=True, halign="left", valign="middle")
        self.puissance.bind(size=self.puissance.setter('text_size'))
        self.labelvitesse = Label(text="[b]Vitesse :[/b]", font_size="30sp", markup=True, halign="right", valign="middle")
        self.labelvitesse.bind(size=self.labelvitesse.setter('text_size'))
        self.vitesse = Label(font_size="30sp", size_hint=(.8, 1), markup=True, halign="left", valign="middle")
        self.vitesse.bind(size=self.vitesse.setter('text_size'))
        self.labelacceleration = Label(text="[b]Accélération :[/b]", font_size="30sp", markup=True, halign="right", valign="middle")
        self.labelacceleration.bind(size=self.labelacceleration.setter('text_size'))
        self.acceleration = Label(font_size="30sp", size_hint=(.8, 1), markup=True, halign="left", valign="middle")
        self.acceleration.bind(size=self.acceleration.setter('text_size'))
        self.labeleclairement = Label(text="[b]Eclairement :[/b]", font_size="30sp", markup=True, halign="right", valign="middle")
        self.labeleclairement.bind(size=self.labeleclairement.setter('text_size'))
        self.eclairement = Label(font_size="30sp", size_hint=(.8, 1), markup=True, halign="left", valign="middle")
        self.eclairement.bind(size=self.eclairement.setter('text_size'))

        self.lonlat = Label(font_size="20sp", markup=True, pos_hint={'center_x': .5, 'center_y': .05})
        self.connexion = Button(text="Connexion (Badge ISEN)", font_size="30sp", background_color=[0, .7, 0, 1], background_normal='', markup=True, on_release=self.read_card)
        self.alert = Label(text="[color=ff3333]Badge ISEN non reconnu ![/color]", font_size="30sp", markup=True)

        # Widget
        self.toolbarlogograph.add_widget(self.logo)
        self.toolbarlogograph.add_widget(self.wifi)
        self.toolbarlogograph.add_widget(self.graphpuissance)
        self.toolbarpuissance.add_widget(self.labelpuissance)
        self.toolbarpuissance.add_widget(self.puissance)
        self.toolbarvitesse.add_widget(self.labelvitesse)
        self.toolbarvitesse.add_widget(self.vitesse)
        self.toolbaracceleration.add_widget(self.labelacceleration)
        self.toolbaracceleration.add_widget(self.acceleration)
        self.toolbareclairement.add_widget(self.labeleclairement)
        self.toolbareclairement.add_widget(self.eclairement)
        self.toolbar.add_widget(self.titre)
        self.toolbar.add_widget(self.toolbarlogograph)
        self.toolbar.add_widget(self.toolbarpuissance)
        self.toolbar.add_widget(self.toolbarvitesse)
        self.toolbar.add_widget(self.toolbaracceleration)
        self.toolbar.add_widget(self.toolbareclairement)
        self.toolbar.add_widget(self.connexion)
        self.layout.add_widget(self.toolbar)
        self.maplayout.add_widget(self.map)

        with self.maplayout.canvas:
            Color(0, 0, 0, .4)
            Rectangle(size=(400, 50))

        self.maplayout.add_widget(self.lonlat)
        self.layout.add_widget(self.maplayout)

        # Clock update
        Clock.schedule_interval(self.update_pos, 1.0 / 30.0)
        Clock.schedule_interval(self.update, 1.001)

        return self.layout

    def on_start(self):
        self.mydb = connect(
            host="localhost",
            user="root",
            passwd="root",
            database="fcity"
        )

        self.rideId = 0
        self.voltageVal = 240
        self.t = 0

        self.cltSock = ClientSocket()

        curs = self.mydb.cursor()

        curs.execute("SELECT r.id as rideId, u.badgeId as badgeId FROM ride as r JOIN users as u ON u.id=r.user_id WHERE r.start_date IS NOT NULL and r.end_date IS NULL and NOW() between r.start_reservation and r.end_reservation")

        res = curs.fetchone()
        curs.close()
        self.mydb.commit()

        if res == None :
            self.cltSock.synchronize()
        else :
            self.rideId = res[0]
            self.cltSock.setCurrentRide(self.rideId)
            self.badgeId = res[1]
            self.toolbar.remove_widget(self.connexion)
            self.initialization()

    def update_rect(self, instance, value):
        self.rect.pos = self.toolbar.pos
        self.rect.size = self.toolbar.size

    def read_card(self, dt):
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
            if match(".*HID.*", device.name):
                dev = InputDevice(device.path)

        try:
            if dev:
                pass
        except:
            return

        # Provided as an example taken from my own keyboard attached to a Centos 6 box:
        scancodes = {
            # Scancode: ASCIICode
            0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
            10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
            20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
            30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
            40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
            50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
        }

        capscodes = {
            0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
            10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
            20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
            30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
            40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
            50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
        }

        #setup vars
        x = ''
        caps = False

        #grab provides exclusive access to the device
        dev.grab()

        #loop
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)  # Save the event temporarily to introspect it
                if data.scancode == 42 or data.scancode == 54:
                    if data.keystate == 1:
                        caps = True
                    if data.keystate == 0:
                        caps = False
                if data.keystate == 1:  # Down events only
                    if caps:
                        key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)  # Lookup or return UNKNOWN:XX
                    else:
                        key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)  # Lookup or return UNKNOWN:XX
                    if (data.scancode != 42) and (data.scancode != 54) and (data.scancode != 28):
                        x += key_lookup
                    if data.scancode == 28:
                        if match("\;[0-9]{16}\?", x):
                            break
                        else:
                            try:
                                self.toolbar.add_widget(self.alert)
                            except:
                                pass
                            return
                        x = ''
        try:
            self.toolbar.remove_widget(self.alert)
        except:
            pass
        self.toolbar.remove_widget(self.connexion)

        self.badgeId = x[11:-1]

        curs = self.mydb.cursor()

        try :
            curs.execute("SELECT r.id from ride as r JOIN users as u on u.id=r.user_id WHERE u.badgeId={} and NOW() BETWEEN r.start_reservation and r.end_reservation".format(self.badgeId))
            res = curs.fetchone()

            self.rideId = res[0]

        except Exception as e:
            self.rideId = -1

        curs.close()

        self.cltSock.setCurrentRide(self.rideId)
        self.cltSock.startRide()

        self.initialization()

    def initialization(self):
        curs = self.mydb.cursor()
        curs.execute("SELECT nickname FROM users WHERE badgeId={}".format(self.badgeId))
        res = curs.fetchone()
        nickname = res[0]

        curs = self.mydb.cursor()

        now = datetime.now()

        curs.execute("UPDATE ride SET start_date = '{}' WHERE id = {}".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.rideId))
        curs.close()
        self.mydb.commit()

        if self.rideId == -1 :
            stoptext = "Pas de trajet réservé"
        else:
            stoptext = "Fin"

        self.user = Label(text="[b]Utilisateur :[/b] {}".format(nickname), font_size="30sp", markup=True)
        self.layout_pause_stop = BoxLayout(orientation="horizontal")
        if self.rideId == -1:
            stoptext = "Pas de trajet réservé"
            self.stop = Button(text=stoptext, font_size="30sp", background_color=[1, 0, 0, 1], background_normal='', markup=True, on_release=self.abort_ride)
        else:
            stoptext = "Fin (Parking ISEN)"
            self.pause = Button(text="Pause", font_size="25sp", size_hint=(.6, 1), background_color=[1, .7, 0, 1], background_normal='', markup=True, on_release=self.pause_ride)
            self.layout_pause_stop.add_widget(self.pause)
            self.stop = Button(text=stoptext, font_size="25sp", background_color=[1, 0, 0, 1], background_normal='', markup=True, on_release=self.stop_ride)
        self.layout_pause_stop.add_widget(self.stop)
        self.toolbar.add_widget(self.user)
        self.toolbar.add_widget(self.layout_pause_stop)

    def abort_ride(self, dt):
        quit()

    def pause_ride(self, dt):
        quit()

    def stop_ride(self, dt):
        self.maplayout.clear_widgets()
        self.toolbar.clear_widgets()
        self.layout.clear_widgets()

        self.popuplayout = BoxLayout()
        self.layout.add_widget(self.popuplayout)
        self.progress = ProgressBar(max=4, value=0)
        self.popup = Popup(title='Transfert des données vers le serveur', content=self.progress)
        self.popuplayout.add_widget(self.popup)

        if self.rideId != -1 :
            curs = self.mydb.cursor()
            now = datetime.now()
            curs.execute("UPDATE ride SET end_date = '{}' WHERE id = {}".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.rideId))
            curs.close()
            self.mydb.commit()

            self.endQ = Queue()
            t = Thread(target=self.cltSock.endRide, args=(self.endQ,))
            t.start()
            self.progress_clock = Clock.schedule_interval(self.next, 1)

    def next(self, dt):
        if not self.endQ.empty():
            self.progress.value = self.endQ.get()

        if self.progress.value == 4 or self.rideId == -1:
            self.progress_clock.cancel()
            quit()

    def update_pos(self, dt):
        if self.rideId > 0 :

            self.lonlat.text = "[color=ffffff][b]Longitude :[/b] {} |  [b]Latitude :[/b] {}[/color]".format(round(self.map.lon, 4), round(self.map.lat, 4))
            self.home.lon = self.map.lon
            self.home.lat = self.map.lat

    def update(self, dt):
        self.titre.text = "[b]GPS FCity[/b] {}".format(datetime.now().strftime("%d/%m/%y %H:%M"))
        self.wifi.text = self.is_connected()[1]

        if self.rideId > 0 :

            self.insertFakeData()

            self.vitesse.text = " {} km/h".format(int(round(self.speedVal)))
            self.acceleration.text = " {} g".format(round(uniform(0, 3), 2))
            self.eclairement.text = " {} lux".format(int(round(randint(500, 100000))))

            self.puiss = self.voltageVal*self.intensityVal
            self.q.put(self.puiss)
            self.puissance.text = " {} W".format(int(round(self.puiss)))

    def insertFakeData(self) :
        self.t += 1

        self.speedVal = round(uniform(20,30)*(sin(self.t*0.01)+1),2)
        self.intensityVal = round(self.speedVal/10,2)

        curs = self.mydb.cursor()
        now = datetime.now()

        curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId,1,self.speedVal,now.strftime('%Y-%m-%d %H:%M:%S')))
        curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId,2,self.voltageVal,now.strftime('%Y-%m-%d %H:%M:%S')))
        curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId,3,self.intensityVal,now.strftime('%Y-%m-%d %H:%M:%S')))

        self.voltageVal = round(self.voltageVal-0.04,2)

        curs.close()
        self.mydb.commit()


    def is_connected(self):
        try:
            host = gethostbyname("google.com")
            create_connection((host, 80), 2)
            return True, "[b][color=#10b200]WIFI ON[/color][/b]"
        except Exception as e:
            return False, "[b][color=#cb0000][s]WIFI OFF[/s][/color][/b]"

