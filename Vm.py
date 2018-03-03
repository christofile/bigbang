!/usr/bin/python
from xml.dom import  minidom
import commands

VMNameLabelList=[]
VcpuMaxList=[]
VcpuStartupList=[]
MemStaMaxList=[]
MemDynMaxList=[]
MemDynMinList=[]
MemStaMinList=[]
VmUuidList=[]
SrUuid=commands.getoutput("xe sr-list type=nfs params=uuid --minimal")

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


DbVMRead("VM","name__label",VMNameLabelList)
DbVMRead("VM","VCPUs__max",VcpuMaxList)
DbVMRead("VM","VCPUs__at_startup",VcpuStartupList)
DbVMRead("VM","memory__static_max",MemStaMaxList)
DbVMRead("VM","memory__dynamic_max",MemDynMaxList)
DbVMRead("VM","memory__dynamic_min",MemDynMinList)
DbVMRead("VM","memory__static_min",MemStaMinList)

for i in range(0,len(VMNameLabelList)):
        VmUuidList.append(VmTemplateInstall(VMNameLabelList[i],SrUuid))
	       VmParamSet(VcpuMaxList[i],VcpuStartupList[1],MemStaMaxList[i],MemDynMaxList[i],MemDynMinList[i],MemStaMinList[i],VmUuidList[i])
