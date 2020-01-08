# -*- coding: utf-8 -*-

from resources.lib import loghelper

import sys
import socket
import selectors
import time

class sReceiver(object):
    "Socket client to Receiver"

    def __init__(self, ip, port=23, timeout=10):
        self.server_addr = (ip, port)
        self.events = selectors.EVENT_READ
        self.data = sData(bytes=0, text=b"")

    def connect(self):
        loghelper.log('Connecting to receiver ' + str(self.server_addr), 'NOTIFICATION_INFO')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(self.server_addr)
        self.sel = selectors.DefaultSelector()
        self.sel.register(sock, self.events, data=self.data)

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
                    self.sel.unregister(sock)
                    sock.close()

class sData(object):
    def __init__(self, bytes=0, text=b""):
        self.bytes = bytes;
        self.text = text;
