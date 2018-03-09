#!/usr/bin/python
from xml.dom import  minidom
import commands


VMMotherUuidList=[]#xs1中vif对应vm的uuid
VMMotherNameLabelList=[]#xs1中vif对应vm的name label
VifMotherList=[]#xs1中vif的uuid
NetworkMotherList=[]#xs1中vif对应network的uuid
NetworkMotherNameLabelList=[]#xs1中vif对应network的name label
VifDeviceNumMotherList=[]#xs1中vif对应device num
NetworkUuidList=[]#xs2中vif对应的network的uuid
VmVifUuidList=[]#xs2中vif对应的vm的uuid

def DbVMRead(TableName,AttributeName,ResultList):
        db = minidom.parse("/tmp/state.db")
        root = db.documentElement
        nodes= root.getElementsByTagName("table")
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                        ResultList.append(m.getAttribute(AttributeName))

#vif对应的vm-uuid和network-uuid均不存放于state.db，而采用OpaqueRef方式关联

#通过network/vm uuid的opaqueref找对应的name label
def DbOpaqueRefFind(TableName,AttributeName,ResultList):
        db = minidom.parse("/tmp/state.db")
        root = db.documentElement
        nodes= root.getElementsByTagName("table")
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("ref")==AttributeName:
                                        ResultList.append(m.getAttribute("name__label"))

DbVMRead("VIF","uuid",VifMotherList)
DbVMRead("VIF","VM",VMMotherUuidList)
DbVMRead("VIF","network",NetworkMotherList)
DbVMRead("VIF","device",VifDeviceNumMotherList)


print VifMotherList
print VMMotherUuidList
print NetworkMotherList
print VifDeviceNumMotherList

for vm in NetworkMotherList:
                DbOpaqueRefFind("network",vm,NetworkMotherNameLabelList)

for vm in VMMotherUuidList:
                DbOpaqueRefFind("VM",vm,VMMotherNameLabelList)


print NetworkMotherNameLabelList
print VMMotherNameLabelList

#通过name label查找对应的uuid，要求name label不同
def NameLabel2Uuid(CmdList,NameLabelList,UuidList):
                for m in NameLabelList:
                                cmd="xe " + CmdList + " name-label=\"" + m + "\" params=uuid --minimal"
                                UuidList.append(commands.getoutput(cmd))

NameLabel2Uuid("network-list",NetworkMotherNameLabelList,NetworkUuidList)
NameLabel2Uuid("vm-list",VMMotherNameLabelList,VmVifUuidList)

print NetworkUuidList
print VmVifUuidList

#创建VIF
def VmVifCreate(NetworkUuid,VmUuid,VifDeviceNum):
                for i in range(0, len(VifMotherList)):
                        VifCreate="xe vif-create vm-uuid=\"" + VmUuid[i] + "\" network-uuid=\"" + NetworkUuid[i] + "\" mac=random device=" + VifDeviceNum[i]                        
				        print VifCreate
                        commands.getoutput(VifCreate)

VmVifCreate(NetworkUuidList,VmVifUuidList,VifDeviceNumMotherList)
