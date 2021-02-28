# BottleWeb-backend

使用Docker统一开发环境

教程：

先安装docker (自行Google), 然后Clone github repo到本地, 建议用vscode打开

以下全部的command都要让terminal进到repo的directory中再输入

（MYSQL部分）

1. 安装Mysql docker
   
   在Terminal中运行： 
   
         docker pull mysql/mysql-server:lastest
   
2. 本地生成运行Mysql容器，Mysql初始用户为root, 密码为设置的123456，容器名设为mysql-server
   
   在Terminal运行：
   
         docker run --name=mysql-server -e MYSQL_ROOT_PASSWORD=123456 -p 3307:3306 -d mysql/mysql-server:latest

3. 进入Mysql容器，创建新用户，数据库和表，并修改密码认证方式（不然docker会报错）
   
   在Terminal运行： 
   
         docker exec -it mysql-server mysql -uroot -p
   
   输入密码123456进入mysql以后运行： 
   
                                 create database mydb;
                                 
                                 create user 'robert'@'%' identified by '123456';
                                 
                                 grant all privileges on mydb.* to 'robert'@'%';
                                 
                                 use mysql;
                                 
                                 ALTER USER 'robert'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
                                 
                                 use mydb;
                                 
                                 create table sys_user (user_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                                                        username VARCHAR(50),
                                                        password VARCHAR(255),
                                                        user_role VARCHAR(10));
                                 
                                 insert into sys_user values (0, 'test', 'test', 'admin');
                                 
                                 quit;

4. 然后创建一个docker network，为后续与bottle的docker相连作准备（理解为在俩docker容器间搭桥通讯)
   
   在Terminal中运行：
   
         docker network create my-network

5. 把刚才搭建好的Mysql容器放到my-network这个桥上
   
   在Terminal中运行：
   
         docker network connect --alias mysql my-network mysql-server
   
6. Mysql部分搭建完毕，然后搭bottle部分，这里需要用到github repo里的Dockerfile

(Bottle部分)

1. 利用Dockerfile生成bottle的docker镜像
   
   在Terminal运行：
   
         sudo docker build -t test:v0 .

2. 利用刚刚生成的docker镜像生成docker容器,容器命名为bottle-backend, 注意--volumn=后面跟的absolute path修改成你电脑里对应的该directory位置
    
   在Terminal运行： 
   
         docker create --name bottle-backend -p 8080:8080 --volume=/home/robert/Desktop/BottleWebsite test:v0

3. 把bottle的容器放上刚刚mysql也在的那个network桥
   
   在Terminal中运行：
   
         docker network connect --alias bottle my-network bottle-backend

4. 运行容器：
   
         docker start bottle-backend

到这就应该OK了


测试API接口是否正常工作：

推荐用POSTMAN，如果 test.py 里面的几个接口都能正常使用就没啥问题了, 注意POSTMAN在测试localhost的时候需要安装运行Postman Agent


Tips:

1. 一共2个docker container：MYSQL和Bottle，container名分别为mysql-server和bottle-backend

2. 修改代码后想测试新功能需要重新创建Bottle部分的docker image和docker container（重过一遍上面的Bottle部分），Mysql那边不用动

3. 新建image的时候 "sudo docker build -t test:v0 ." 里面的 "test:v0", test是image主名，v0是tag，以后新建image可以命名为test:v1等以此类推

4. 在利用Dockerfile新建image的时候先不要开vpn，不然docker跑RUN pip3 install那些指令的时候会连不上网（DNS问题），如果已经开了VPN再关掉然后发现连不上网可以试试sudo systemctl restart docker，不行就直接重启电脑吧（Ubuntu我试了好多其他方法都不得劲0.0)

5. 新建container的时候container名不能使用已经用过的名字，除非删掉那个对应的container

6. 几个常用的docker command: 

         docker ps 正在运行的container
   
         docker images 已创建的docker镜像
   
         docker inspect CONTAINER-NAME 查看对应container的详细信息（比如看里头的network部分）
   
         docker rmi $(docker images -f dangling=true -q) 删除多余的docker images(不然很占电脑空间）
   
         docker rm CONTAINER-NAME 删除对应的container
               
7. 建议还是想办法按上一个repo把环境在本地搭好，那个搭环境可比docker省事儿多了0.0，docker这玩意用来部署网站的时候打包更方便一点，开发的时候用这个还是有点蛋疼，import个新的包还得改Dockerfile然后重建image，听说有办法直接基于Docker环境做开发，还没了解

8. 建议全程使用VSC，Pycharm好像老是出现奇奇怪怪的问题
                                          
                  
