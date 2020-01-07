import telnetlib
import socket

from time import sleep

class ReceiverException(Exception):
    pass

class Receiver(object):
    "Telnet client to Receiver"

    def __init__(self, ip, port=23, timeout=10):
        try:
            self.tn = telnetlib.Telnet(ip, port)
        except socket.timeout:
            raise ReceiverException("Error connecting to device")

    def __sendcmd__(self, cmd):
        "Sends single command to AV"""
        command = cmd + '\r\n'

        self.tn.read_eager() # Cleanup any pending output.
        self.tn.write(command)
        sleep(0.1) # Cool-down time (taken from github/PioneerRebel)
        return self.tn.read_eager().replace('\r\n', '');

    def isOn(self):
        "Returns true if device is on"""
        status = self.__sendcmd__("?P")

        if status == "PWR0":
            return True
        else:
            return False

    def getVol(self):
        "Returns device volume in device scale 0-80"""
        vol_string = self.__sendcmd__("?V")
        vol_sub = vol_string[3:]
        return ( int(vol_sub) - 1 ) / 2.0

    def getVolPer(self):
        "Returns device volume in 0-100 scale"""
        vol = self.getVol( )
        vol_dec = float(vol) + 1.25
        return vol_dec

    def close(self):
        self.tn.close()
