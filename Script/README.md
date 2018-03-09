# bigbang
Code for 2015 Bigbang

设计
1. 前端：Dijango
1) 用户注册登陆
2）选择需要的lab类型，时间

2. 后端：Apache+MySQL+Python+Redis
1) 根据用户提交信息，查询是否有可用XenServer
2) XenServer上部署虚拟机(VmCreate.py)
3) 虚拟机部署完成后邮件通知用户(postfix)
4) Lab 到期后销毁(VmDestroy.py)

流程
WorkFlow.jpg
