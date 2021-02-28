# BottleWeb-backend

使用Docker统一开发环境

教程：

先安装docker (自行Google)

以下全部的command都要让terminal进到repo的directory中输入

（MYSQL部分）

1. Clone github repo到本地, 建议用vscode打开

2. 安装Mysql docker
   在Terminal中运行： docker pull mysql/mysql-server:lastest
   
3. 本地生成运行Mysql容器，Mysql初始用户为root, 密码为设置的123456，容器名设为mysql-server
   在Terminal运行： docker run --name=mysql-server -e MYSQL_ROOT_PASSWORD=123456 -p 3307:3306 -d mysql/mysql-server:latest

4. 进入Mysql容器，创建新用户，数据库和表，并修改密码认证方式（不然docker会报错）
   在Terminal运行： docker exec -it mysql-server mysql -uroot -p
   输入密码123456进入mysql以后运行： create database mydb;
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

5. 然后创建一个docker network，为后续与bottle的docker相连作准备（理解为在俩docker容器间搭桥通讯)
   在Terminal中运行：docker network create my-network

6. 把刚才搭建好的Mysql容器放到my-network这个桥上
   在Terminal中运行：docker network connect --alias mysql my-network mysql-server
   
7. Mysql部分搭建完毕，然后搭bottle部分，这里需要用到github repo里的Dockerfile

(Bottle部分)

1. 利用Dockerfile生成bottle的docker镜像
   在Terminal运行：sudo docker build -t test:v0 .

2. 利用刚刚生成的docker镜像生成docker容器,容器命名为bottle-backend, 注意--volumn=后面跟的absolute path修改成你电脑里对应的该directory位置
    在Terminal运行： docker create --name bottle-backend -p 8080:8080 --volume=/home/robert/Desktop/BottleWebsite test:v0

3. 把bottle的容器放上刚刚mysql也在的那个network桥
   在Terminal中运行：docker network connect --alias bottle my-network bottle-backend

4. 运行容器：
   docker start bottle-backend

OK了，缺了啥再补上，你们先试一下
                   
  
                                          
                  
   
    
