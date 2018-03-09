#!/usr/bin/python
import commands
import os

#Destroy VM
VMUuid=commands.getoutput("xe vm-list is-a-template=false is-control-domain=false is-a-snapshot=false params=uuid --minimal")

print VMUuid

VMUuidList=VMUuid.split(",")

print VMUuidList

for vm in VMUuidList:
        os.system("xe vm-destroy uuid=" + vm)
		
#Destroy VDI
SrUuid=commands.getoutput("xe sr-list type=nfs params=uuid --minimal")

VdiUuid=commands.getoutput("xe vdi-list sr-uuid=" + SrUuid + " params=uuid --minimal")

VdiUuidList=VdiUuid.split(",")

for vdi in VdiUuidList:
		os.system("xe vdi-destroy uuid=" + vdi)

#Destroy Network
XapiBridgeList=[]
XapiUuidList=[]

NetBridge=commands.getoutput("xe network-list params=bridge --minimal")

NetBridgeList=NetBridge.split(",")

for bridge in NetBridgeList:
		bri=bridge.find("xapi")
		if bri >= 0:
				XapiBridgeList.append(bridge)

print XapiBridgeList
				
for xapi in XapiBridgeList:
		XapiUuid=commands.getoutput("xe network-list bridge=" + xapi + " params=uuid --minimal")
                XapiUuidList.append(XapiUuid)
		
print XapiUuidList

for uuid in XapiUuidList:
		os.system("xe network-destroy uuid=" + uuid)
		

