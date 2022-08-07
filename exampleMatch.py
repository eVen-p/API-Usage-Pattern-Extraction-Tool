import javalang
from py2neo import Graph
from py2neo import Node
from py2neo import Relationship
from py2neo import NodeMatcher


# 读取java文件
fd = open("D:\JavaWorkspace\API\example3.java", "r", encoding="utf-8")  
tree = javalang.parse.parse(fd.read())            
fd.close()

# output.write(str(tree.types[0].body[0]))

apiList = []
for function in tree.types[0].body:
    for sentence in function.body:
        flag = 0
        try:
            t = sentence.declarators[0].initializer
            flag = 1
        except:
            flag = 2
            apiList.append(str(sentence.expression.member))
        
        if flag == 1:
            try:
                apiList.append(str(t.member))
            except:
                print(str(t))
                if t:
                    apiList.append(str(t.arguments[0].member))

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474', auth=("neo4j","123456"))
tx = graph.begin()
#graph.delete_all()

codeList = []
#print(apiList)

for i in apiList:
    tempNode = Node('function',name=i)
    matcher = NodeMatcher(graph)
    isMatch = list(matcher.match('function',name=i))
    #print(isMatch)
    if isMatch:
        codeList.append(i)
        
#print(codeList)
graph.commit(tx)

fd2 = open("D:\JavaWorkspace\API\example3.java", "r", encoding="utf-8")  
lines = fd2.readlines()

fd_write = open("D:\JavaWorkspace\\code3.txt", "w", encoding="utf-8")

dict = {"aaaaaa":0}
count = 1

for line in lines:
    for name in codeList:
        if name in line:
            tokens = line.split()
            if "=" in tokens:
                ind = tokens.index("=")
                id = tokens[ind-1]
                dict[id] = count
                count += 1

            for k in dict.keys():
                if k in line:
                    #print("----")
                    #print("k=" + k + ":" + str(dict[k]))
                    #print(type(line))
                    hole = "<" + str(dict[k]) + ">"
                    line = line.replace(k,hole)    
                    #print(line)        

            fd_write.write(line)

fd2.close()
fd_write.close()





