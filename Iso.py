#!/usr/bin/python
from xml.dom import  minidom
import commands

VmUuidList=['efad503b-4985-3199-b564-b20d755addc3', '8446f12c-692c-607e-5271-62d19f6dc39e', '82284685-58ed-844d-35d3-0ce4a9cf13f3']


def VmISOVbdCreate(VmUuid,DiskDeviceNum):

        ISOCreate="xe vbd-create vm-uuid=" + VmUuid + " device=" + DiskDeviceNum + " type=CD mode=RO bootable=false"
        commands.getoutput(ISOCreate)


for vm in VmUuidList:
                 VmISOVbdCreate(vm,"1")
