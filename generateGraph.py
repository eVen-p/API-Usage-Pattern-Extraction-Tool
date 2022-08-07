import javalang
from py2neo import Graph
from py2neo import Node
from py2neo import Relationship
from py2neo import NodeMatcher
from py2neo import RelationshipMatcher

# 读取java文件
fd = open("D:\JavaWorkspace\\3.java", "r", encoding="utf-8")  
tree = javalang.parse.parse(fd.read())            
fd.close()

# output.write(str(tree.types[0].body[0]))

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474', auth=("neo4j","123456"))
tx = graph.begin()
graph.delete_all()

nodeList = []
nodeDictionnary = {}

for method in tree.types[0].body:
    modifiers = method.modifiers
    if 'public' in modifiers:
        # can be an API
        APIname = method.name
        APIparameters = method.parameters
        APIreturntype = method.return_type
        APInode = Node('function',name=APIname)
        nodeList.append(APInode)
        graph.create(APInode)

        # handling return type
        if type(APIreturntype) == javalang.tree.ReferenceType:
            if not APIreturntype.name in nodeDictionnary:
                typeNode = Node('type',name=APIreturntype.name)
                graph.create(typeNode)
                relation = Relationship(APInode,"use",typeNode)
                graph.create(relation)
                
                nodeDictionnary[APIreturntype.name] = typeNode
            else:
                typeNode = nodeDictionnary[APIreturntype.name]
                relation = Relationship(APInode,"use",typeNode)
                graph.create(relation)

        #handling parameters list
        for para in APIparameters:
            paraType = para.type.name
            if not paraType in nodeDictionnary:
                typeNode = Node('type',name=paraType)
                graph.create(typeNode)
                relation = Relationship(typeNode,"use",APInode)
                graph.create(relation)
                nodeDictionnary[paraType] = typeNode
            else:
                typeNode = nodeDictionnary[paraType]
                relation = Relationship(typeNode,"use",APInode)
                graph.create(relation)

# 为同一个类内部的函数添加协作关系
for node in nodeList:
    for node2 in nodeList:
        if node != node2:
            relation = Relationship(node,"coorperate",node2)
            graph.create(relation)

graph.commit(tx)




