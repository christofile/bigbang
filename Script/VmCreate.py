#!/usr/bin/python
from xml.dom import  minidom
import commands
import time


#Variable declaration Region


PrivateNetworkList=[]  #private network name label list in mother xs

VMNameLabelList=[]
VcpuMaxList=[]
VcpuStartupList=[]
MemStaMaxList=[]
MemDynMaxList=[]
MemDynMinList=[]
MemStaMinList=[]
VmUuidList=[]      # uuid of vm on son xs

VMMotherUuidList=[]#vm uuid of vif in mother xs
VMMotherNameLabelList=[]#vm name label of vif in mother xs
VifMotherList=[]#vif uuid in mother xs
NetworkMotherList=[]#network uuid of vif in mother xs
NetworkMotherNameLabelList=[]#network name label of vif in mother xs
VifDeviceNumMotherList=[]#device num of vif in mother xs
NetworkUuidList=[]#network uuid of vif in son xs
VmVifUuidList=[]#vm uuid of vif in son xs

VMRefList=[] #vm opaque ref list
VMVdiRefList=[]
VMDiskSize=[]
######Python xml

#for mother xs
db = minidom.parse("/tmp/state.db")
root = db.documentElement
nodes= root.getElementsByTagName("table")


#Part 1:Read db data

###Step 0:Read default SR uuid(from son xs)####
def SrUuidRead():
        sr="xe sr-list type=nfs params=uuid --minimal"
        SrUuid=commands.getoutput(sr)
        return SrUuid

SrUuid=SrUuidRead()
###Step 1: Create private network ###

def DbNetworkRead(TableName,AttributeName,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                        if "xapi" in m.getAttribute(AttributeName):
                                                ResultList.append(m.getAttribute("name__label"))

DbNetworkRead("network","bridge",PrivateNetworkList)

for network in PrivateNetworkList:
        PNCreate="xe network-create name-label=" + network
        commands.getoutput(PNCreate)

###Step 2: Create vm and set param###
def DbVMRead(TableName,AttributeName,ResultList):
    for n in nodes:
        if n.getAttribute("name")==TableName:
            row=n.getElementsByTagName("row")
            for m in row:
                        if m.getAttribute("is_a_snapshot")=="false" and m.getAttribute("is_a_template")=="false" and m.getAttribute("is_control_domain")=="false":
                                ResultList.append(m.getAttribute(AttributeName))


DbVMRead("VM","name__label",VMNameLabelList)
DbVMRead("VM","VCPUs__max",VcpuMaxList)
DbVMRead("VM","VCPUs__at_startup",VcpuStartupList)
DbVMRead("VM","memory__static_max",MemStaMaxList)
DbVMRead("VM","memory__dynamic_max",MemDynMaxList)
DbVMRead("VM","memory__dynamic_min",MemDynMinList)
DbVMRead("VM","memory__static_min",MemStaMinList)

def VmTemplateInstall(VMNameLabelList,SrUuid):
        VmInstall="xe vm-install new-name-label=" + VMNameLabelList + " sr-uuid=" + SrUuid + " template=Other\ install\ media"
        VmUuid=commands.getoutput(VmInstall)
        return VmUuid 

def VmParamSet(VcpuMax,VcpuStartup,MemStaMax,MemDynMax,MemDynMin,MemStaMin,VmUuid):
        MSMax=str(int(MemStaMax)/1024/1024)
        MDMax=str(int(MemDynMax)/1024/1024)
        MDMin=str(int(MemDynMin)/1024/1024)
        MSMin=str(int(MemStaMin)/1024/1024)

        VmCpuSet="xe vm-param-set VCPUs-max=" + VcpuMax + " VCPUs-at-startup=" + VcpuStartup + " uuid=" + VmUuid
        VmMSMaxSet="xe vm-param-set memory-static-max=" + MSMax + "MiB" + " uuid=" + VmUuid
        VmMDMaxSet="xe vm-param-set memory-dynamic-max=" + MDMax + "MiB" + " uuid=" + VmUuid
        VmMDMinSet="xe vm-param-set memory-dynamic-min=" + MDMin + "MiB" + " uuid=" + VmUuid
        VmMSMinSet="xe vm-param-set memory-static-min=" + MSMin + "MiB" + " uuid=" + VmUuid

        commands.getoutput(VmCpuSet)
        commands.getoutput(VmMSMaxSet)
        commands.getoutput(VmMDMaxSet)
        commands.getoutput(VmMDMinSet)
        commands.getoutput(VmMSMinSet)

for i in range(0,len(VMNameLabelList)):
        VmUuidList.append(VmTemplateInstall(VMNameLabelList[i],SrUuid))
        VmParamSet(VcpuMaxList[i],VcpuStartupList[1],MemStaMaxList[i],MemDynMaxList[i],MemDynMinList[i],MemStaMinList[i],VmUuidList[i])

time.wait(5)

###Step 3: Create disk ###

def DbVMRead(TableName,AttributeName,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                        if m.getAttribute("is_a_snapshot")=="false" and m.getAttribute("is_a_template")=="false" and m.getAttribute("is_control_domain")=="false":
                                                        ResultList.append(m.getAttribute(AttributeName))


DbVMRead("VM","ref",VMRefList)


def DbVdiFind(TableName,AttributeName,AttributeNameFind,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("VM")==AttributeName and m.getAttribute("type")=="Disk":
                                        ResultList.append(m.getAttribute(AttributeNameFind))

def DbDiskSizeFind(TableName,AttributeName,AttributeNameFind,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("ref")==AttributeName:
                                        ResultList.append(m.getAttribute(AttributeNameFind))

for vm in VMRefList:
                DbVdiFind("VBD",vm,"VDI",VMVdiRefList)


for vm in VMVdiRefList:
                DbDiskSizeFind("VDI",vm,"virtual_size",VMDiskSize)

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


###Step 4: Create iso###
def VmISOVbdCreate(VmUuid,DiskDeviceNum):

        ISOCreate="xe vbd-create vm-uuid=" + VmUuid + " device=" + DiskDeviceNum + " type=CD mode=RO bootable=false"
        commands.getoutput(ISOCreate)


for vm in VmUuidList:
                 VmISOVbdCreate(vm,"1")
				 
###Step 5: Create vif ###

def DbVMRead(TableName,AttributeName,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                        ResultList.append(m.getAttribute(AttributeName))

DbVMRead("VIF","uuid",VifMotherList)
DbVMRead("VIF","VM",VMMotherUuidList)
DbVMRead("VIF","network",NetworkMotherList)
DbVMRead("VIF","device",VifDeviceNumMotherList)

print VifMotherList
print VMMotherUuidList
print NetworkMotherList
print VifDeviceNumMotherList


def DbOpaqueRefFind(TableName,AttributeName,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("ref")==AttributeName:
                                        ResultList.append(m.getAttribute("name__label"))



for vm in NetworkMotherList:
                DbOpaqueRefFind("network",vm,NetworkMotherNameLabelList)

for vm in VMMotherUuidList:
                DbOpaqueRefFind("VM",vm,VMMotherNameLabelList)

print NetworkMotherNameLabelList
print VMMotherNameLabelList
				
				
def NameLabel2Uuid(CmdList,NameLabelList,UuidList):
                for m in NameLabelList:
                                cmd="xe " + CmdList + " name-label=\"" + m + "\" params=uuid --minimal"
                                UuidList.append(commands.getoutput(cmd))

NameLabel2Uuid("network-list",NetworkMotherNameLabelList,NetworkUuidList)
NameLabel2Uuid("vm-list",VMMotherNameLabelList,VmVifUuidList)

print NetworkUuidList
print VmVifUuidList

def VmVifCreate(NetworkUuid,VmUuid,VifDeviceNum):
                for i in range(0, len(VifMotherList)):
                        VifCreate="xe vif-create vm-uuid=\"" + VmUuid[i] + "\" network-uuid=\"" + NetworkUuid[i] + "\" mac=random device=" + VifDeviceNum[i]
			print VifCreate
                        commands.getoutput(VifCreate)

VmVifCreate(NetworkUuidList,VmVifUuidList,VifDeviceNumMotherList)


