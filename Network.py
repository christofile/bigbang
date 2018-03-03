#!/usr/bin/python
from xml.dom import  minidom
import commands

PrivateNetwork=[]
db = minidom.parse("/tmp/state.db")
root = db.documentElement
nodes= root.getElementsByTagName("table")
for n in nodes:
    if n.getAttribute("name")=="network":
        row=n.getElementsByTagName("row")
        for m in row:
                if "xapi" in m.getAttribute("bridge"):
                        PrivateNetwork.append(m.getAttribute("name__label"))

#provision private network

for network in PrivateNetwork:
        cmd="xe network-create name-label=" + network
        commands.getoutput(cmd)