# coding=utf-8

__author__ = "Peter Boraros <pborky@pborky.sk>"

#    Copyright (C) 2013 Peter Boraros <pborky@pborky.sk>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from threading import Thread
from Queue import Queue,Empty,Full

class Enum:
    """Base class for enums
    """
    class __metaclass__(type):
        def __new__(mcs, name, bases, attrs):
            Meta = attrs.get('Meta')
            if getattr(Meta,'reverse_mapping', True):
                reverse = {}
            else:
                reverse = None
            for key in attrs:
                val = attrs[key]
                if callable(val):
                    if val.__name__=='__init__':
                        raise Exception('Not expecting instances')
                    if not isinstance(val, classmethod):
                        attrs[key] = classmethod(val) # not expecting instances !
                else:
                    if isinstance(val,tuple) and len(val) == 2:
                        val,resource = val
                    else:
                        resource = None
                    if reverse is not None:
                        if  val in reverse:
                            raise Exception('Non unique value, cannot setup reverse mapping')
                        reverse[val] = key, resource
            if reverse is not None:
                attrs['reverse'] = reverse.get
            attrs.update(getattr(Meta,'attrs', {}))
            return type.__new__(mcs, name, bases, attrs)


class R:
    class string:
        effect_no_effect = 0
        effect_pulse = 1
        effect_random = 2
        effect_zoetrope = 3
        effect_alert = 4
        effect_candle = 5
        effect_light_fire = 6
        effect_police = 7
        effect_fireplace = 8
        effect_fire = 9
        effect_rgb = 10
        backlight_no_backlight = 11
        backlight_on = 12
        backlight_pulse = 13
        color_set_mode_continually = 14
        color_set_mode_hard = 15
        color_set_mode_transition = 16
        off = 17
        lamp_intensity = 18
        hide_pallete_after_applying_color = 19
        title_dialog_pallete = 20
        pallete_button_clear = 21
        toast_cannot_connect_to_bluetooth_lamp = 22
        pallete = 23
        select_lamp = 24
        dialog_title_select_color_set_mode = 25
        toast_disconnected = 26
        lamp_disconnected = 27
        lamp_lightness = 28
        lamp_humidity = 29
        lamp_temperature = 30
        lamp_discovering = 31
        lamp_select_backlight_effect = 32
        lamp_select_effect = 33
        dialog_cancel = 34
        toast_could_not_connect = 35
        lamp_connecting = 36
        lamp_disconnect = 37
        lamp_connect = 38
        button_turn_off = 39
        choose_bluetooth_device = 40
        app_name = 41

class Strings:
    LANGUAGE_ENGLISH = 0
    LANGUAGE_CZECH = 1
    CURRENT_LANGUAGE = LANGUAGE_ENGLISH
    _l = {
        R.string.backlight_no_backlight: ("No backlight", "Bez podsvícení" ),
        R.string.backlight_on: ("Backlight On",	"Zapnout podsvícení" ),
        R.string.backlight_pulse: ("Pulse", "Pulzování" ),
        R.string.color_set_mode_continually: ("Continually", "Průběžné" ),
        R.string.color_set_mode_hard: ("Hard", "Rychlé" ),
        R.string.color_set_mode_transition: ("Transition", "Přechod" ),
        R.string.effect_alert: ("Alert", "Upozornění"),
        R.string.effect_police: ("Police", "Policie"),
        R.string.effect_pulse: ("Pulse", "Pulzování"),
        R.string.effect_random: ("Random", "Náhodný efekt"),
        R.string.effect_rgb: ("Random color", "Náhodná barva"),
        R.string.effect_zoetrope: ("Zoetrope", "Stroboskop"),
        R.string.effect_candle: ("Candle", "Svíčka"),
        R.string.effect_fire: ("Fire", "Oheň"),
        R.string.effect_fireplace: ("Fireplace", "Ohniště"),
        R.string.effect_light_fire: ("Light Fire", "Jemný oheň"),
        R.string.effect_no_effect: ("No Effect", "Žádný efekt"),
        R.string.off: ("Off", "Vypnuto"),
        R.string.lamp_intensity: ("Intensity: ", "Intenzita: "),
        R.string.toast_cannot_connect_to_bluetooth_lamp: ("Cannot connect to lamp", "Nelze se připojit k lampičce"),
        R.string.pallete: ("Color Pallete", "Barevná paleta"),
        R.string.select_lamp: ("Choose Moody Light", "Vyberte Náladovou Lampičku"),
        R.string.dialog_title_select_color_set_mode: ("Color Set Mode", "Způsob použití barvy"),
        R.string.toast_disconnected: ("You have been disconnected", "Byli jste odpojeni"),
        R.string.lamp_disconnected: ("Disconnected", "Odpojeno"),
        R.string.lamp_lightness: ("Lightness: ", "Světelnost: "),
        R.string.lamp_humidity: ("Humidity: ", "Vlhkost: "),
        R.string.lamp_temperature: ("Temperature: ", "Teplota: "),
        R.string.lamp_select_backlight_effect: ("Select Backlight Effect", "Vybrat režim podsvícení"),
        R.string.lamp_select_effect: ("Select Effect", "Vybrat efekt"),
        R.string.dialog_cancel: ("Cancel", "Zrušit"),
        R.string.lamp_connecting: ("Connecting", "Připojování"),
        R.string.lamp_disconnect: ("Disconnect", "Odpojit"),
        R.string.lamp_connect: ("Connect", "Připojit"),
        R.string.button_turn_off: ("Switch Off", "Vypnout"),
        R.string.app_name: ("Lamp Controller", "Ovladač Lampičky"),
    }
    @classmethod
    def getString(cls, r):
        if r in cls._l:
            return cls._l.get(r)
        else:
            return "Unknown string %d"%r

class BluetoothLampBacklightMode(Enum):
    OFF     = 0, R.string.backlight_no_backlight
    ON      = 1, R.string.backlight_on
    PULSE   = 2, R.string.backlight_pulse

class BluetoothLampEffect(Enum):
    NO_EFFECT   = 0, R.string.effect_no_effect
    PULSE       = 1, R.string.effect_pulse
    RANDOM      = 2, R.string.effect_random
    ZOETROPE    = 3, R.string.effect_zoetrope
    ALERT       = 4, R.string.effect_alert
    CANDLE      = 5, R.string.effect_candle
    LIGHT_FIRE  = 6, R.string.effect_light_fire
    POLICE      = 10, R.string.effect_police
    FIREPLACE   = 11, R.string.effect_fireplace
    FIRE        = 12, R.string.effect_fire
    RGB         = 13, R.string.effect_rgb

class LampSettings(object):
    def __init__(self,red,green,blue,currentBacklightEffect,currentEffect,currentColorIntensity):
        self.red = red
        self.green = green
        self.blue = blue
        self.currentBacklightEffect = currentBacklightEffect
        self.currentEffect = currentEffect
        self.currentColorIntensity = currentColorIntensity

class BluetoothLampCommand(Enum):
    ACTION_BACKLIGHT_SET_EFFECT = "A"
    ACTION_GET_LAMP_ID = "I 2"
    ACTION_GET_LAMP_INFO = "I 0"
    ACTION_SET_EFFECT = "x"
    ACTION_SET_COLOR_WITH_CROSS_FADE = "c"
    ACTION_SET_COLOR_HARD = "r"
    ACTION_GET_LAMP_VERSION = "I 3"
    ACTION_GET_LAMP_SERIAL_NUMBER = "I 1"
    ACTION_GET_LAMP_CURRENT_SETTINGS = "I 4"
    ACTION_SET_COLOR_INTENSITY = "p"
    class Meta:
        import re
        reverse_mapping = False
        attrs = {  # TODO: replace with BNF-capable parser
            'LAMP_INFO': re.compile(r"^0 ([-]?[0-9]|[-]?[1-9][0-9]|[-]?100):([0-9]|[1-9][0-9]|100):(10[0-2][0-4]|[1-9][1-9][0-9]|[1-9][0-9]|[0-9])$"),
            'LAMP_NAME': re.compile(r"^2 .*$"),
            'LAMP_VERSION': re.compile(r"^3 .*$"),
            'LAMP_SERIAL': re.compile(r"^1 [0-9]{8}$"),
            'LAMP_SETTINGS': re.compile(r"^4 .*$"),
        }
    @classmethod
    def parse_line(cls, line, *args, **kwargs):  # TODO: replace with BNF-capable parser
        result = kwargs
        line = line.strip()
        if cls.LAMP_INFO.match(line):
            result['LAMP_INFO'] = line
        elif cls.LAMP_NAME.match(line):
            result['LAMP_NAME'] = line[2:]
        elif cls.LAMP_VERSION.match(line):
            result['LAMP_VERSION'] = line[2:]
        elif cls.LAMP_SERIAL.match(line):
            result['LAMP_SERIAL'] = line[2:]
        elif cls.LAMP_SETTINGS.match(line):
            settings = line[2:].split(':')
            if settings and len(settings) == 6:
                result['LAMP_SETTINGS'] =LampSettings(*settings)
        return result

class Color(Enum):
    BLACK = 0xFF000000
    DKGRAY = 0xFF444444
    GRAY = 0xFF888888
    LTGRAY = 0xFFCCCCCC
    WHITE = 0xFFFFFFFF
    RED = 0xFFFF0000
    GREEN = 0xFF00FF00
    BLUE = 0xFF0000FF
    YELLOW = 0xFFFFFF00
    CYAN = 0xFF00FFFF
    MAGENTA = 0xFFFF00FF
    TRANSPARENT = 0

    @classmethod
    def alpha(cls, color):
        return (color & 0xFF000000) >> 24
    @classmethod
    def red(cls, color):
        return (color & 0xFF0000) >> 16
    @classmethod
    def green(cls, color):
        return (color & 0xFF00) >> 8
    @classmethod
    def blue(cls, color):
        return color & 0xFF

class BluetoothLampCommandListener(Thread):
    def __init__(self, receiveCallback, **kwargs):
        super(BluetoothLampCommandListener, self).__init__(**kwargs)
        self.daemon = True
        self.receiveCallback = receiveCallback
        self.queue = Queue(1)
        self.readOnly = False
    def sendData(self, data):
        if not self.readOnly:
            self.queue.put_nowait(data)
        else:
            raise Exception('Command listener is read-only.')
    def setReadOnly(self, readOnly):
        print 'read-only' if readOnly else 'read-write'
    def handleReceivedLine(self, line):
        self.receiveCallback(line)
    def run(self):
        while True:
            try:
                item = self.queue.get(block=True,timeout=0.1)
                if item.startswith(BluetoothLampCommand.ACTION_GET_LAMP_ID):
                    pass
                elif item.startswith(BluetoothLampCommand.ACTION_GET_LAMP_INFO):
                    self.handleReceivedLine('0 20:60:100')
                elif item.startswith(BluetoothLampCommand.ACTION_SET_EFFECT):
                    pass
                elif item.startswith(BluetoothLampCommand.ACTION_BACKLIGHT_SET_EFFECT):
                    pass
                elif item.startswith(BluetoothLampCommand.ACTION_SET_COLOR_WITH_CROSS_FADE):
                    pass
                elif item.startswith(BluetoothLampCommand.ACTION_SET_COLOR_HARD):
                    pass
                elif item.startswith(BluetoothLampCommand.ACTION_GET_LAMP_VERSION):
                    self.handleReceivedLine('3 0.0.0')
                elif item.startswith(BluetoothLampCommand.ACTION_GET_LAMP_SERIAL_NUMBER):
                    self.handleReceivedLine('1 00000000')
                elif item.startswith(BluetoothLampCommand.ACTION_GET_LAMP_CURRENT_SETTINGS):
                    self.handleReceivedLine('4 0:0:0:0:0:0')
                elif item.startswith(BluetoothLampCommand.ACTION_SET_COLOR_INTENSITY):
                    pass
                else:
                    pass

            except Empty:
                pass

class SerialTranciever(object):
    pass

class BluetoothLamp(object):
    def __init__(self):
        self.listener = BluetoothLampCommandListener(self.receiveLine)
        self.data = {}
        self.listener.start()
    def receiveLine(self, line):
        self.data.update(BluetoothLampCommand.parse_line(line))
        print self.data
    def getCurrentSettings(self):
        """Requests current lamp settings"""
        self.listener.sendData(BluetoothLampCommand.ACTION_GET_LAMP_CURRENT_SETTINGS)
    def getLampId(self):
        """Returns lamp name (id)"""
        self.listener.sendData(BluetoothLampCommand.ACTION_GET_LAMP_ID)
    def getLampInfo(self):
        """Returns lamp informations (format #<temperature:humidity:light_level:666>"""
        self.listener.sendData(BluetoothLampCommand.ACTION_GET_LAMP_INFO)
    def getLampSerial(self):
        """Returns lamp serial number (4 hex-digits)"""
        self.listener.sendData(BluetoothLampCommand.ACTION_GET_LAMP_SERIAL_NUMBER)
    def getLampVersion(self):
        """Returns lamp name version"""
        self.listener.sendData(BluetoothLampCommand.ACTION_GET_LAMP_VERSION)
    def setBacklightEffect(self, effect):
        """Sets backlight effect"""
        self.listener.sendData("%s %s" % (
                BluetoothLampCommand.ACTION_BACKLIGHT_SET_EFFECT,
                effect
            ))
    def setColorHard(self, color=None, red=None, green=None, blue=None):
        """Sets color without effect
        @param color Integer of color 0xRRGGBB
        @param red 0-255
        @param green 0-255
        @param blue 0-255
        """
        if color is not None:
            red = Color.red(color)
            green = Color.green(color)
            blue = Color.blue(color)
        self.listener.sendData("%s %d %d %d" %(BluetoothLampCommand.ACTION_SET_COLOR_HARD, red, green, blue))
    def setColorIntensity(self, intensity):
        """Sets color intensity
        @param intensity 0-10"""
        self.listener.sendData("%s %d" %( BluetoothLampCommand.ACTION_SET_COLOR_INTENSITY, intensity))
    def setColorWithCrossFade(self, color=None, red=None, green=None, blue=None):
        """Sets color with cross-fade effect
        @param color Integer of color 0xRRGGBB
        @param red 0-255
        @param green 0-255
        @param blue 0-255
        """
        if color is not None:
            red = Color.red(color)
            green = Color.green(color)
            blue = Color.blue(color)
        self.listener.sendData("%s %d %d %d" % (BluetoothLampCommand.ACTION_SET_COLOR_WITH_CROSS_FADE, red, green, blue))
    def setEffect(self, effect):
        """Runs given effect
        @param effect (@see BluetoothLampEffect)
        """
        self.listener.sendData("%s %s" %(BluetoothLampCommand.ACTION_SET_EFFECT, effect))
    def setReadOnly(self, readOnly):
        """Turns off communication
        @param readOnly true to turn off writes
        """
        self.listener.setReadOnly(readOnly)
