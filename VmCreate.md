虚拟机四大块：机器模版，内存和cpu,网卡信息，磁盘信息

全局创建

1. 创建相同存储上的sr
xe sr-create host-uuid=6485c911-b97d-4824-bf6f-fbd1881ebcd9 type=nfs shared=true device-config:server=10.158.144.10 device-config:serverpath=/nfs name-label=PublicNfs

2. 创建母版相同的private network
xe network-create name-label=test 


对于每个虚拟机创建

1. 创建空的vm模版
xe vm-install new-name-label=CentOS64 sr-uuid=f75a6206-f728-2eda-a005-fa60620b8d7f template=Other\ install\ media

2. 配置cpu和memory
xe vm-param-set VCPUs-max=1 VCPUs-at-startup=1 uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f
xe vm-param-set memory-static-min=512MiB uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f 
xe vm-param-set memory-dynamic-min=512MiB uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f 
xe vm-param-set memory-dynamic-max=512MiB uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f 
xe vm-param-set memory-static-max=512MiB uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f 


3. 创建网络和网卡
xe network-list 
xe vif-create vm-uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f network-uuid=2c8b057b-4520-5d3f-12a7-08bbfddd5681 mac=random device=0
xe vif-create vm-uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f network-uuid=59e74314-62a5-83d1-dc99-9f08bab72ee7 mac=random device=1


4. 创建磁盘和iso
xe vm-disk-add sr-uuid=f75a6206-f728-2eda-a005-fa60620b8d7f device=0 disk-size=8GiB uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f 
xe vbd-param-set uuid=9a24c0b8-7fc7-deb2-f553-64229dc5872d  bootable=true

xe vbd-create vm-uuid=e7812b6b-1973-dc54-65dd-069cf4c3527f device=1 type=CD mode=RO bootable=false


磁盘创建必须为FV，然后在共享存储中将

 INTERNAL_ERROR: [ Failure("Failed to parse device name: ") ]
