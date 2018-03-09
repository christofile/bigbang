from xml.dom import  minidom

#以下代码实现输出所有pbd的uuid
db = minidom.parse("/var/xapi/state.db") #得到dom对象
root = db.documentElement #得到文档元素对象，获得根元素（database）
nodes= root.getElementsByTagName("table") #读取子元素
for n in nodes: 
    if n.getAttribute("name")=="PBD": #得到元素属性值
        row=n.getElementsByTagName("row")
        for m in row:
                print m.getAttribute("uuid")