# Dépot contenant les sources de l'application Kivy du tableau de bord FCity, le serveur FCity et la base de données

## Installation de Kivy sur le Raspberry Pi 3 b+
https://kivy.org/doc/stable/installation/installation-rpi.html

`sudo apt update`

`sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev python-setuptools libgstreamer1.0-dev git-core gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} python-dev libmtdev-dev xclip xsel`

`sudo apt install python3-pip`

`sudo pip3 install -U Cython`

`sudo pip3 install git+https://github.com/kivy/kivy.git@stable-1.10`

`sudo pip3 install kivy-garden`

`garden install mapview`

`garden install graph`

`sudo pip3 install evdev`

`sudo pip3 install pyserial`

`sudo pip3 install mysql-connector`

`sudo apt install mysql-server`

`sudo pip3 install protobuf`

## Rotation de l'écran, désactivation splash screen, activation le l'uart en déactivant le bluetooth
`vim /boot/config.txt`

lcd_rotate=2

disable_splash=1

dtoverlay=pi3-disable-bt

## Suppression logo au démarrage
`vim /boot/cmdline.txt`

logo.nologo

## Insertion de la base de données

`mysql -u root -p < fcity-dump-timestamp-ms.sql`

## Démarrage du programme NavigationApp.py au démarrage du Raspberry Pi
`sudo cp fcity.service /lib/systemd/system/.`

`sudo systemctl enable fcity.service`

## Démarrage du programme server.py au démarrage du serveur (A exécuter sur le serveur)
`sudo cp fcity-server.service /lib/systemd/system/.`

`sudo systemctl enable fcity-server.service`

## Activation de l'écran tactile dans Kivy
`vim ~/.kivy/config.ini`

[input]

mouse = mouse

mtdev_%(name)s = probesysfs,provider=mtdev

hid_%(name)s = probesysfs,provider=hidinput

## Changer le fuseau horaire
`sudo dpkg-reconfigure tzdata`

## Configuration Wi-Fi ISEN
`sudo vim /etc/wpa_supplicant/wpa_supplicant.conf`

country=FR

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev

update_config=1

network={

ssid="ISEN"
 
key_mgmt=WPA-EAP
        
eap=PEAP
        
identity="identifiant ISEN"
        
password="mot de passe ISEN"
        
phase2="auth=MSCHAPV2"

}
