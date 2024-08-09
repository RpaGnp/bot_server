import os
import socket
import sys
from getpass import getuser


class GetInfPC():
    def __init__(self):
        self.IpPc = None
        self.NomPc = None
        self.SesPc = None

    def getNom(self):
        return socket.gethostname()

    def getIp(self):
        return socket.gethostbyname(self.getNom())

    def getUsu(self):
        return getuser()

    def getInfpC(self):
        return [self.getIp(), self.getNom(), self.getUsu()]
