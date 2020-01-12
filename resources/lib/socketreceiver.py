# -*- coding: utf-8 -*-

from resources.lib import loghelper

import socket
import selectors
import time
import urllib2

class sReceiver(object):
    "Socket client to Receiver"

    def __init__(self, ip, port=23, start_url = '', stop_url = ''):
        self.server_addr = (ip, port)
        self.events = selectors.EVENT_READ
        self.data = sData(bytes=0, text=b"")
        self.connected = False
        self.start_url = False if start_url == '' else start_url
        self.stop_url = False if stop_url == '' else stop_url

    def connect(self, timeout=10):
        loghelper.log('Connecting to receiver ' + repr(self.server_addr), 'NOTIFICATION_INFO')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.settimeout(timeout)
        try:
            sock.connect(self.server_addr)
        except Exception as ex:
            self.connected = False
            loghelper.log("Could not connect to receiver on " + repr(self.server_addr) + ": " + str(ex) , 'NOTIFICATION_ERROR')
            return False
        else:
            self.connected = True
            self.sel = selectors.DefaultSelector()
            self.sel.register(sock, self.events, data=self.data)
            if self.start_url:
                loghelper.log('Connecting to IFTTT start url: ' + self.start_url, 'NOTIFICATION_INFO')
                self.hitUrl(self.start_url)
            loghelper.log("Connected to receiver " + repr(self.server_addr), 'NOTIFICATION_INFO')
            return True

    def disconnect (self, sock):
        self.sel.unregister(sock)
        sock.close()
        if self.stop_url:
            loghelper.log('Connecting to IFTTT stop url: ' + self.start_url, 'NOTIFICATION_INFO')
            self.hitUrl(self.stop_url)

    def listener_service(self, key, mask, delay = 1):
        sock = key.fileobj
        self.data = key.data
        if mask & selectors.EVENT_READ:
            # Should be ready to read
            recv_data = sock.recv(1024);
            if recv_data:
                self.data.bytes = len(recv_data)
                self.data.text = recv_data.decode()
                # Check if the received data is a volume change an display it.
                pos = self.data.text.rfind("VOL")
                if  pos > -1:
                    vol_num = int(self.data.text[pos+3:pos+6])
                    offset = -80
                    vol = (( int(vol_num) - 1 ) / 2.0 ) + offset
                    loghelper.log('Volume changed: ' + str(vol), 'VOLUME_CHANGE')
                    # Add a delay till the next read to prevent spamming
                    time.sleep(delay)
                # If we receive the power down signal close the connection
                elif self.data.text.rfind("PWR1") > -1:
                    loghelper.log('Receiver shutting down.', 'NOTIFICATION_INFO')
                    self.disconnect(sock)

    def hitUrl(self, url):
        try:
            urllib2.urlopen(url).read()
        except Exception as ex:
            loghelper.log("Could not connect to url " + url + ": " + str(ex) , 'NOTIFICATION_ERROR')

class sData(object):
    def __init__(self, bytes=0, text=b""):
        self.bytes = bytes;
        self.text = text;
