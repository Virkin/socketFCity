#!/usr/bin/python3

# Classe MainSreen qui controle l'ecran principal de l'application
# Elle est compose de deux parties distinctes : les donnees a gauche et la carte a droite

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
from time import time
from evdev import InputDevice, categorize, ecodes, list_devices
from re import match
from datetime import datetime
from clientClass import ClientSocket
from mysql.connector import connect
from math import sin
from threading import Thread
from queue import Queue
from socket import gethostbyname, create_connection
from json import load
from serial import Serial
from os import system


class MainScreen(Screen):
    def __init__(self, q, **kwargs):
        """ initilisation de l'ecran """
        super(MainScreen, self).__init__(**kwargs)
        self.layoutmain = RelativeLayout()
        self.layoutmain.add_widget(self.build())
        self.on_start()
        self.add_widget(self.layoutmain)
        self.q = q

    def switchtograph(self, *args):
        """ changement vers l'ecran graphique  """
        self.manager.transition.direction = "left"
        self.manager.current = "graph"

    def build(self):
        """ construction de l'interface de l'ecran principal """
        # definition des zones de l'ecran
        self.layout = BoxLayout(orientation="horizontal")
        self.toolbar = BoxLayout(orientation="vertical")
        self.toolbarlogograph = BoxLayout(orientation="horizontal")
        self.toolbarpuissance = BoxLayout(orientation="horizontal")
        self.toolbarvitesse = BoxLayout(orientation="horizontal")
        self.toolbaracceleration = BoxLayout(orientation="horizontal")
        self.toolbareclairement1 = BoxLayout(orientation="horizontal")
        self.toolbareclairement2 = BoxLayout(orientation="horizontal")
        self.toolbareclairement3 = BoxLayout(orientation="horizontal")
        self.maplayout = RelativeLayout()
        # ajout d'une image d'arriere plan sur la partie gauche
        #with self.toolbar.canvas.before:
        #    Color(1, 1, 1, .5)
        #    self.rect = Rectangle(size=self.toolbar.size, pos=self.toolbar.pos, source="fcity.jpg")
        #self.toolbar.bind(pos=self.update_rect, size=self.update_rect)

        # construction de la carte sur la patie droite
        self.map = MapView(zoom=16, lat=48.406970, lon=-4.495254, map_source="osm-fr")
        # ajout des bornes de recharges provenant du ficher json
        with open('bornes-recharge.json') as json_file:
             data = load(json_file)
             for k, v in data.items():
                 self.map.add_marker(MapMarker(lon=v["lon"], lat=v["lat"], source="img/charging-station.png"))
        # ajout de la position actuelle de la voiture
        self.home = MapMarker(lat=48.406970, lon=-4.495254)
        self.map.add_marker(self.home)


        # creation des etiquettes contenenant les donnees de la voiture
        self.titre = Label(text="[b]GPS FCity[/b] {}".format(datetime.now().strftime("%d/%m/%y %H:%M")), font_size="30sp", markup=True)
        self.battery = Image(source="img/battery-full.png")
        self.wifi = Image(source="")
        # bouton premettant de changer d'ecran vers le graphique
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
        self.labeleclairement1 = Label(text="[b]Eclairement 1 :[/b]", font_size="30sp", markup=True, halign="right", valign="middle")
        self.labeleclairement1.bind(size=self.labeleclairement1.setter('text_size'))
        self.eclairement1 = Label(font_size="30sp", size_hint=(.8, 1), markup=True, halign="left", valign="middle")
        self.eclairement1.bind(size=self.eclairement1.setter('text_size'))
        self.labeleclairement2 = Label(text="[b]Eclairement 2 :[/b]", font_size="30sp", markup=True, halign="right", valign="middle")
        self.labeleclairement2.bind(size=self.labeleclairement2.setter('text_size'))
        self.eclairement2 = Label(font_size="30sp", size_hint=(.8, 1), markup=True, halign="left", valign="middle")
        self.eclairement2.bind(size=self.eclairement2.setter('text_size'))
        self.labeleclairement3 = Label(text="[b]Eclairement 3 :[/b]", font_size="30sp", markup=True, halign="right", valign="middle")
        self.labeleclairement3.bind(size=self.labeleclairement3.setter('text_size'))
        self.eclairement3 = Label(font_size="30sp", size_hint=(.8, 1), markup=True, halign="left", valign="middle")
        self.eclairement3.bind(size=self.eclairement3.setter('text_size'))


        self.lonlat = Label(font_size="20sp", markup=True, pos_hint={'center_x': .5, 'center_y': .05})
        # bouton de connexion avec le lecteur de badge ISEN
        self.connexion = Button(text="Connexion (Badge ISEN)", font_size="30sp", background_color=[0, .7, 0, 1], background_normal='', markup=True, on_release=self.read_card)
        self.alert = Label(text="[color=ff3333]Badge ISEN non reconnu ![/color]", font_size="30sp", markup=True)

        # ajout des modules a l'ecran principal
        self.toolbarlogograph.add_widget(self.battery)
        self.toolbarlogograph.add_widget(self.wifi)
        self.toolbarlogograph.add_widget(self.graphpuissance)
        self.toolbarpuissance.add_widget(self.labelpuissance)
        self.toolbarpuissance.add_widget(self.puissance)
        self.toolbarvitesse.add_widget(self.labelvitesse)
        self.toolbarvitesse.add_widget(self.vitesse)
        self.toolbaracceleration.add_widget(self.labelacceleration)
        self.toolbaracceleration.add_widget(self.acceleration)
        self.toolbareclairement1.add_widget(self.labeleclairement1)
        self.toolbareclairement1.add_widget(self.eclairement1)
        self.toolbareclairement2.add_widget(self.labeleclairement2)
        self.toolbareclairement2.add_widget(self.eclairement2)
        self.toolbareclairement3.add_widget(self.labeleclairement3)
        self.toolbareclairement3.add_widget(self.eclairement3)
        self.toolbar.add_widget(self.titre)
        self.toolbar.add_widget(self.toolbarlogograph)
        self.toolbar.add_widget(self.toolbarpuissance)
        self.toolbar.add_widget(self.toolbarvitesse)
        self.toolbar.add_widget(self.toolbaracceleration)
        self.toolbar.add_widget(self.toolbareclairement1)
        self.toolbar.add_widget(self.toolbareclairement2)
        self.toolbar.add_widget(self.toolbareclairement3)
        self.toolbar.add_widget(self.connexion)
        self.layout.add_widget(self.toolbar)
        self.maplayout.add_widget(self.map)

        with self.maplayout.canvas:
            Color(0, 0, 0, .4)
            Rectangle(size=(400, 50))

        self.maplayout.add_widget(self.lonlat)
        self.layout.add_widget(self.maplayout)

        # creation de boucles de mises a jour
        Clock.schedule_interval(self.update_pos, 1.0 / 30.0)
        Clock.schedule_interval(self.update, 1)

        # connexion en uart avec le stm32 qui recupere les donnees de la voiture
        self.serial0 = Serial("/dev/serial0", baudrate=9600, timeout=0.05)

        return self.layout

    def on_start(self):
        """ connexion a la base de donnees """
        self.mydb = connect(
            host="localhost",
            user="root",
            passwd="root",
            database="fcity"
        )

        self.rideId = 0
        self.connect = False

        curs = self.mydb.cursor()

        # recuperation du numero du trajet et du numero de badge de l'utilisateur
        curs.execute("SELECT r.id as rideId, u.badgeId as badgeId FROM ride as r JOIN users as u ON u.id=r.user_id WHERE r.start_date IS NOT NULL and r.end_date IS NULL and NOW() between r.start_reservation and r.end_reservation")

        res = curs.fetchone()
        curs.close()
        self.mydb.commit()

        if res == None :
            self.cltSock = ClientSocket()
            self.cltSock.synchronize()
            self.connect = True
        else :
            self.rideId = res[0]
            self.badgeId = res[1]
            self.toolbar.remove_widget(self.connexion)
            self.initialization()

    def update_rect(self, instance, value):
        """ mise a jour des images"""
        self.rect.pos = self.toolbar.pos
        self.rect.size = self.toolbar.size

    def read_card(self, dt):
        """ lecture du numero du badge ISEN """
        devices = [InputDevice(path) for path in list_devices()]
        # selection du bon peripherique
        for device in devices:
            if match(".*HID.*", device.name):
                dev = InputDevice(device.path)

        try:
            if dev:
                pass
        except:
            return

        # conversion des codes du lecteur de badge en caracteres ASCII
        scancodes = {
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

        x = ''
        caps = False

        # utilise le peripherique uniquement pour l'application 
        dev.grab()

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
                        # badge ISEN detecte
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

        # recuperation du numero dans une variable
        self.badgeId = x[11:-1]

        curs = self.mydb.cursor()

        try :
            # verification du trajet de l'utilsateur avant le demarrage
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
        # recuperation du pseudo avec le numero de badge
        curs.execute("SELECT nickname FROM users WHERE badgeId={}".format(self.badgeId))
        res = curs.fetchone()
        nickname = res[0]

        curs = self.mydb.cursor()

        now = datetime.now()

        # mise a jour du debut du trajet
        curs.execute("UPDATE ride SET start_date = '{}' WHERE id = {}".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.rideId))
        curs.close()
        self.mydb.commit()

        if self.rideId == -1 :
            stoptext = "Pas de trajet réservé"
        else:
            stoptext = "Fin"

        # affichage du pseudo de l'utilisateur sur l'ecran
        self.user = Label(text="[b]Utilisateur :[/b] {}".format(nickname), font_size="30sp", markup=True)
        self.layout_pause_stop = BoxLayout(orientation="horizontal")
        # arret de l'application si l'utilisateur n'a pas reserve de trajet
        if self.rideId == -1:
            stoptext = "Pas de trajet réservé"
            self.stop = Button(text=stoptext, font_size="30sp", background_color=[1, 0, 0, 1], background_normal='', markup=True, on_release=self.stop_ride)
            self.layout_pause_stop.add_widget(self.stop)
        # creation des boutons pause et fin de trajet si l'utilisateur a reserve un trajet
        else:
            stoptext = "Fin (Parking ISEN)"
            self.stop = Button(text=stoptext, font_size="25sp", background_color=[1, 0, 0, 1], background_normal='', markup=True, on_release=self.stop_ride)
            self.layout_pause_stop.add_widget(self.stop)
            self.pause = Button(text="Pause", font_size="25sp", size_hint=(.6, 1), background_color=[1, .7, 0, 1], background_normal='', markup=True, on_release=self.pause_ride)
            self.layout_pause_stop.add_widget(self.pause)

            self.dataQueue = Queue()
            # demarrage du thread recuperant les donnees du vehicule
            self.receiveData = Thread(target=self.get_data, args=(self.dataQueue,))
            self.receiveData.start()

        self.toolbar.add_widget(self.user)
        self.toolbar.add_widget(self.layout_pause_stop)


    def abort_ride(self, dt):
        system("sudo shutdown now")

    def pause_ride(self, dt):
        system("sudo shutdown now")

    def stop_ride(self, dt):
        """ affichage d'une barre de progression et transfert des donnees vers le serveur """
        if self.is_connected():
            self.maplayout.clear_widgets()
            self.toolbar.clear_widgets()
            self.layout.clear_widgets()

            self.popuplayout = BoxLayout()
            self.layout.add_widget(self.popuplayout)
            self.progress = ProgressBar(max=4, value=0)
            self.popup = Popup(title='Transfert des données vers le serveur', content=self.progress)
            self.popuplayout.add_widget(self.popup)

            self.endQ = Queue()

            if self.rideId != -1 :

                curs = self.mydb.cursor()
                now = datetime.now()
                # mise a jour de la date de fin de trajet
                curs.execute("UPDATE ride SET end_date = '{}' WHERE id = {}".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.rideId))
                curs.close()
                self.mydb.commit()

                t = Thread(target=self.cltSock.endRide, args=(self.endQ,))
                t.start()
                # mise a jour de la barre de progression

            self.progress_clock = Clock.schedule_interval(self.next, 0.1)

    def next(self, dt):
        """ arret du systeme une fois les donnees transferees"""
        if not self.endQ.empty():
            self.progress.value = self.endQ.get()

        if self.progress.value == 4 or self.rideId == -1:
            self.progress_clock.cancel()
            self.cltSock.closeSocket()
            system("sudo shutdown now")

    def update_pos(self, dt):
        """ mise a jour des coordonnees gps sur la carte """
        if self.rideId > 0 :

            self.lonlat.text = "[color=ffffff][b]Longitude :[/b] {} | [b]Latitude :[/b] {}[/color]".format(round(self.map.lon, 4), round(self.map.lat, 4))
            self.home.lon = self.map.lon
            self.home.lat = self.map.lat

    def update(self, dt):
        """ mise a jour des informations et des donnees de l'ecran principal """
        self.maxVoltage = 83

        self.titre.text = "[b]GPS FCity[/b] {}".format(datetime.now().strftime("%d/%m/%y %H:%M"))

        # affiche si le systeme est connecte au serveur
        if self.is_connected() :
            self.wifi.source = "img/wifi-on.png"
            try:
                self.stop.background_color = [1, 0, 0, 1]
            except:
                pass
        else :
            self.wifi.source = "img/wifi-off.png"
            try:
                self.stop.background_color = [0.7, 0, 0, 1]
            except:
                pass


        if self.rideId > 0 :

            if not self.dataQueue.empty() :

                # recuperation des donnees
                self.data = self.dataQueue.get()
                print(self.data)
                try:
                    self.insertData()

                    # mise a jour de la position de la carte
                    if "lat" in self.data and "lon" in self.data:
                        self.map.center_on(float(self.data["lat"]), float(self.data["lon"]))

                    if "vit" in self.data:
                        self.vitesse.text = " {} km/h".format(int(round(float(self.data["vit"]))))
                    if "pn1" in self.data:
                        self.eclairement1.text = " {} lux".format(int(round(float(self.data["pn1"]))))
                    if "pn2" in self.data:
                        self.eclairement2.text = " {} lux".format(int(round(float(self.data["pn2"]))))
                    if "pn3" in self.data:
                        self.eclairement3.text = " {} lux".format(int(round(float(self.data["pn3"]))))
                    if "volt" in self.data:
                        # mise a jour du niveau de batterie
                        self.voltageVal = float(self.data["volt"])

                        if self.voltageVal < self.maxVoltage/8 :
                            self.battery.source = "img/battery-empty.png"
                        elif self.voltageVal >= self.maxVoltage/8 and self.voltageVal < 3*self.maxVoltage/8 :
                            self.battery.source = "img/battery-quarter.png"
                        elif self.voltageVal >= 3*self.maxVoltage/8 and self.voltageVal < 5*self.maxVoltage/8 :
                            self.battery.source = "img/battery-half.png"
                        elif self.voltageVal >= 5*self.maxVoltage/8 and self.voltageVal < 7*self.maxVoltage/8 : 
                            self.battery.source = "img/battery-three-quarters.png"
                        else :
                            self.battery.source = "img/battery-full.png"
                    if "volt" in self.data and "int" in self.data :
                        self.puiss = float(self.data["volt"])*float(self.data["int"])
                        self.puissance.text = " {} W".format(self.puiss)
                        self.q.put(self.puiss)

                    if "accel" in self.data :
                        self.acceleration.text = " {} g".format(self.data["accel"])
                except Exception as e:
                    print(e)

    def insertData(self):
        """ insertion des donnees """
        curs = self.mydb.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        if "vit" in self.data:
            print("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 1, self.data["vit"], now))
            curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 1, self.data["vit"], now))

        if "pn1" in self.data:
            print("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 4, self.data["pn1"], now))
            curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 4, self.data["pn1"], now))

        if "pn2" in self.data:
            print("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 5, self.data["pn2"], now))
            curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 5, self.data["pn2"], now))

        if "pn3" in self.data:
            print("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 7, self.data["pn3"], now))
            curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 7, self.data["pn3"], now))

        if "volt" in self.data:
            print("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 2, self.data["volt"], now))
            curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 2, self.data["volt"], now))

        if "int" in self.data:
            print("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 3, self.data["int"], now))
            curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 3, self.data["int"], now))

        if "accel" in self.data:
            print("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 6, self.data["accel"], now))
            curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 6, self.data["accel"], now))

        curs.close()
        self.mydb.commit()

    def insertFakeData(self) :
        """ generation et insertion de donnees aleatoires """
        self.t += 1

        self.speedVal = round(uniform(20,30)*(sin(self.t*0.01)+1),2)
        self.intensityVal = round(self.speedVal/10,2)

        curs = self.mydb.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 1, self.speedVal, now))
        curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 2, self.voltageVal, now))
        curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.rideId, 3, self.intensityVal, now))

        self.voltageVal = round(abs(self.voltageVal),2)

        curs.close()
        self.mydb.commit()

    def get_data(self, dataQueue):
        """ recuperation en uart des donnees de la voiture """
        data = {}

        if self.stop.text == "Fin (Parking ISEN)":
            while True:
                try:
                    if self.serial0.read().decode("utf-8") == "$":
                        
                        fieldName = ["heu","lat","lon","vit","pn1","pn2","pn3","int","volt","accel"]

                        i=0

                        dataQueue.put(data)
                        for elm in str(self.serial0.readline().decode("utf-8")).split(",") :
                            try:
                                
                                if match("[0-9]+\.[0-9]+(N|S)", elm) or match("[0-9]+\.[0-9]+(W|E)", elm) :
                                    data[fieldName[i]] = dmmToDd(elm)
                                elif i==0 and match("[0-9]+\.[0-9]+", elm) :
                                    heure = trame[0].split(".")[0]
                                    data[fieldName[i]] = "{}:{}:{}".format(heure[:2], heure[2:4], heure[4:])
                                elif match("[0-9]+\.[0-9]+", elm) :
                                    data[fieldName[i]] = elm

                                i += 1

                            except Exception as e :
                                i += 1

                except Exception as e:
                    print(e)

    def is_connected(self):
        """ verification de la connexion au serveur """

        try:
            host = gethostbyname("google.com")
            create_connection((host, 80), 2)

            if not self.connect :
                self.cltSock = ClientSocket()
                self.cltSock.setCurrentRide(self.rideId)
                self.connect = True
            
            return True
        except Exception as e:
            self.connect = False
            return False

def dmmToDd(dmm) :
    dotPos = dmm.find('.')

    d = int(dmm[:dotPos-2])
    m = float(dmm[dotPos-2:-1])
    c = dmm[-1]

    dd = d + float(m)/60
    
    if c=="S" or c=="W" : dd = -dd

    return dd


