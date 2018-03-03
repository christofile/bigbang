#!/usr/bin/python
from xml.dom import  minidom
import commands
import os
import pexpect

VMNameLabelList=[]
VdiMotherUuidList=[]
VdiSonUuidList=[]
#MotherSrUuid='b070558d-53a6-6c15-0c98-973375f0c80e'
#NewSrUuid='f75a6206-f728-2eda-a005-fa60620b8d7f'
DdCommandList=[]

VMRefList=[]
VMVdiRefList=[]

db = minidom.parse("/lab/state.db")
root = db.documentElement
nodes= root.getElementsByTagName("table")

def MortherSrUuidRead(TableName,AttributeName):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("type")==AttributeName:
                                        Result=m.getAttribute("uuid")
			       return Result

MotherSrUuid=MortherSrUuidRead("SR","nfs")

print MotherSrUuid 

def SrUuidRead():
        sr="xe sr-list type=nfs params=uuid --minimal"
        SonSrUuid=commands.getoutput(sr)
        return SonSrUuid

SonSrUuid=SrUuidRead()

print SonSrUuid

def DbVMRead(TableName,AttributeName,ResultList):
    for n in nodes:
        if n.getAttribute("name")==TableName:
            row=n.getElementsByTagName("row")
            for m in row:
                        if m.getAttribute("is_a_snapshot")=="false" and m.getAttribute("is_a_template")=="false" and m.getAttribute("is_control_domain")=="false":
                                ResultList.append(m.getAttribute(AttributeName))


DbVMRead("VM","name__label",VMNameLabelList)

print VMNameLabelList

def VMVdiRead(VmNameLabel,VdiUuidList):
	VmVdi="xe vbd-list vm-name-label=" + VmNameLabel +" params=vdi-uuid type=Disk --minimal"
	VdiUuidList.append(commands.getoutput(VmVdi))

for vm in VMNameLabelList:
	VMVdiRead(vm,VdiSonUuidList)

print VdiSonUuidList

def DbVMRead(TableName,AttributeName,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                        if m.getAttribute("is_a_snapshot")=="false" and m.getAttribute("is_a_template")=="false" and m.getAttribute("is_control_domain")=="false":
                                                        ResultList.append(m.getAttribute(AttributeName))


DbVMRead("VM","ref",VMRefList)

print VMRefList

def DbVdiFind(TableName,AttributeName,AttributeNameFind,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("VM")==AttributeName and m.getAttribute("type")=="Disk":
                                        ResultList.append(m.getAttribute(AttributeNameFind))

for vm in VMRefList:
                DbVdiFind("VBD",vm,"VDI",VMVdiRefList)

print VMVdiRefList

def DbVdiUuidFind(TableName,AttributeName,ResultList):
        for n in nodes:
                if n.getAttribute("name")==TableName:
                        row=n.getElementsByTagName("row")
                        for m in row:
                                if m.getAttribute("ref")==AttributeName:
                                        ResultList.append(m.getAttribute("uuid"))


for vm in VMVdiRefList:
		DbVdiUuidFind("VDI",vm,VdiMotherUuidList)	

print VdiMotherUuidList


for i in range(0,len(VdiMotherUuidList)):
        DdCommandList.append("dd if=/mnt/tscloudlab/lily/demolab/" + MotherSrUuid + "/" + VdiMotherUuidList[i] + ".vhd of=/mnt/tscloudlab/lily/demo-xs62-5/" + SonSrUuid + "/" + VdiSonUuidList[i] + ".vhd")


def ssh_cmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=20)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret

for i in range(0,len(DdCommandList)):
        ssh_cmd('192.168.10.7','111111', str(DdCommandList[i]))

print DdCommandList
