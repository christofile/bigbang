#!/usr/bin/python
from xml.dom import  minidom
import commands



VmUuidList=['efad503b-4985-3199-b564-b20d755addc3', '8446f12c-692c-607e-5271-62d19f6dc39e', '82284685-58ed-844d-35d3-0ce4a9cf13f3']
SrUuid="f75a6206-f728-2eda-a005-fa60620b8d7f"
VMRefList=[]
VMVdiRefList=[]
VMDiskSize=[]

def DbVMRead(TableName,AttributeName,ResultList):
        db = minidom.parse("/tmp/state.db")
        root = db.documentElement
        nodes= root.getElementsByTagName("table")
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                        if m.getAttribute("is_a_snapshot")=="false" and m.getAttribute("is_a_template")=="false" and m.getAttribute("is_control_domain")=="false":
                                                        ResultList.append(m.getAttribute(AttributeName))

DbVMRead("VM","ref",VMRefList)

print VMRefList

def DbVdiFind(TableName,AttributeName,AttributeNameFind,ResultList):
        db = minidom.parse("/tmp/state.db")
        root = db.documentElement
        nodes= root.getElementsByTagName("table")
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("VM")==AttributeName and m.getAttribute("type")=="Disk":
                                        ResultList.append(m.getAttribute(AttributeNameFind))

def DbDiskSizeFind(TableName,AttributeName,AttributeNameFind,ResultList):
        db = minidom.parse("/tmp/state.db")
        root = db.documentElement
        nodes= root.getElementsByTagName("table")
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("ref")==AttributeName:
                                        ResultList.append(m.getAttribute(AttributeNameFind))

for vm in VMRefList:
                DbVdiFind("VBD",vm,"VDI",VMVdiRefList)

print VMVdiRefList

for vm in VMVdiRefList:
                DbDiskSizeFind("VDI",vm,"virtual_size",VMDiskSize)

print VMDiskSize

#创建vm对应的vdi，并且这是vbd的参数
def VmDiskCreate(SrUuid,VmUuid,DiskSize,DiskDeviceNum):

        DS=str(int(DiskSize)/1024/1024/1024)

        DiskCreate="xe vm-disk-add sr-uuid=" + SrUuid + " device=" + DiskDeviceNum + " disk-size=" + DS +"GiB uuid=" + VmUuid
        commands.getoutput(DiskCreate)

        VbdCmd="xe vbd-list vm-uuid=" + VmUuid + " params=uuid --minimal"
        DiskVbdUuid=commands.getoutput(VbdCmd)

        SetBootable="xe vbd-param-set uuid=" + DiskVbdUuid + " bootable=true"
        commands.getoutput(SetBootable)

for i in range(0,len(VmUuidList)):
                VmDiskCreate(SrUuid,VmUuidList[i],VMDiskSize[i],"0")
