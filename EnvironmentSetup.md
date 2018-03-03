
Component Version:			
	1. Django	1.6.5			
	2. Mysql	5.1.73			
	3. Redis	2.6.14			
				

Detail Process:

	1. Install django
	# tar xvf Django-1.6.5.tgz
	# cd Django-1.6.5
	# python setup.py install
	
	2. Verify the installation
	# python
	Python 2.6.6 (r266:84292, Feb 22 2013, 00:00:18) 
	[GCC 4.4.7 20120313 (Red Hat 4.4.7-3)] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import django
	>>> django.VERSION
	(1, 6, 5, 'final', 0)
	
	3. Create project
	# mkdir /lab
	# cd /lab
	# django-admin.py startproject demolab
	

	4. Install mysql
	# yum install mysql mysql-server mysql-devel python-devel
	
	# wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz
	# tar xvf setuptools-0.6c11.tar.gz 
	# cd setuptools-0.6c11
	# python setup.py build
	# python setup.py install
	
	# wget http://sourceforge.net/projects/mysql-python/files/mysql-python/1.2.3/MySQL-python-1.2.3.tar.gz
	# tar xvf MySQL-python-1.2.3.tar.gz 
	# cd MySQL-python-1.2.3
	# ls /usr/bin/ | grep mysql_config
	# vi site.cfg 
	mysql_config = /usr/bin/mysql_config
	# yum install gcc -y
	# python setup.py build
	# python setup.py install
	
	
	# service mysqld start
	# chkconfig mysqld on
	# mysql
	
	mysql> create database demolab;
	Query OK, 1 row affected (0.00 sec)
	
	# vi /lab/demolab/demolab/settings.py
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'demolab',
	        'USER': 'root',
	        'PASSWORD': '',
	        'HOST': 'localhost',
	        'PORT': '3306',
	
	        }
	}
	
	# python /lab/demolab/manage.py shell
	Python 2.6.6 (r266:84292, Jul 23 2015, 15:22:56) 
	[GCC 4.4.7 20120313 (Red Hat 4.4.7-11)] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	(InteractiveConsole)
	>>> from django.db import connection
	>>> cursor=connection.cursor()
	>>> 
	
	4. Template setting
	# vi ./demolab/settings.py
	TEMPLATE_DIRS = (
	        '/lab/demolab/templates',
	)
	# mkdir templates
	
	5. Create the model
	# cd /lab/demolab/
	# python manage.py startapp demolabapp
	# vi ./demolabapp/models.py 
	class User(models.Model):
	    email = models.CharField(max_length=128)
	    password = models.CharField(max_length=32)
	    status = models.CharField(max_length=32)
	    create_time = models.DateTimeField()
	    group = models.CharField(max_length=32)
	    account = models.IntegerField()
	
	class order(models.Model):
	    user_id = models.IntegerField()
	    account_id = models.IntegerField()
	    lab_id = models.IntegerField()
	    start_time = models.DateTimeField()
	    end_time = models.DateTimeField()
	    status = models.CharField(max_length=32)
	
	class lab(models.Model):
	    name = models.CharField(max_length=256)
	    type = models.CharField(max_length=64)
	    description = models.TextField()
	    hypervisor_ip = models.IPAddressField()
	    status = models.CharField(max_length=32)
	    create_time = models.DateTimeField()
	    mail_to_user = models.TextField()
	
	
	# vi ./demolab/settings.py
	INSTALLED_APPS = (
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'demolabapp'
	)
	
	
	# python manage.py validate
	0 errors found
	# python manage.py sqlall demolabapp
	BEGIN;
	CREATE TABLE `demolabapp_user` (
	    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
	    `email` varchar(128) NOT NULL,
	    `password` varchar(32) NOT NULL,
	    `status` varchar(32) NOT NULL,
	    `create_time` datetime NOT NULL,
	    `group` varchar(32) NOT NULL,
	    `account` integer NOT NULL
	)
	;
	CREATE TABLE `demolabapp_order` (
	    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
	    `user_id` integer NOT NULL,
	    `account_id` integer NOT NULL,
	    `lab_id` integer NOT NULL,
	    `start_time` datetime NOT NULL,
	    `end_time` datetime NOT NULL,
	    `status` varchar(32) NOT NULL
	)
	;
	CREATE TABLE `demolabapp_lab` (
	    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
	    `name` varchar(256) NOT NULL,
	    `type` varchar(64) NOT NULL,
	    `description` longtext NOT NULL,
	    `hypervisor_ip` char(15) NOT NULL,
	    `status` varchar(32) NOT NULL,
	    `create_time` datetime NOT NULL,
	    `mail_to_user` longtext NOT NULL
	)
	;
	
	COMMIT;
	# python manage.py syncdb
	Creating tables ...
	Creating table django_admin_log
	Creating table auth_permission
	Creating table auth_group_permissions
	Creating table auth_group
	Creating table auth_user_groups
	Creating table auth_user_user_permissions
	Creating table auth_user
	Creating table django_content_type
	Creating table django_session
	Creating table demolabapp_user
	Creating table demolabapp_order
	Creating table demolabapp_lab
	
	You just installed Django's auth system, which means you don't have any superusers defined.
	Would you like to create one now? (yes/no): yes
	Username (leave blank to use 'root'): 
	Email address: liang333916@126.com
	Password: 
	Password (again): 
	Superuser created successfully.
	Installing custom SQL ...
	Installing indexes ...
	Installed 0 object(s) from 0 fixture(s)
	[root@controller demolab]# mysql
	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 5
	Server version: 5.1.73 Source distribution
	
	Copyright (c) 2000, 2013, Oracle and/or its affiliates. All rights reserved.
	
	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.
	
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	
	mysql> show databases;
	+--------------------+
	| Database           |
	+--------------------+
	| information_schema |
	| demolab            |
	| mysql              |
	| test               |
	+--------------------+
	4 rows in set (0.00 sec)
	
	mysql> use demolab
	Reading table information for completion of table and column names
	You can turn off this feature to get a quicker startup with -A
	
	Database changed
	mysql> show tables;
	+----------------------------+
	| Tables_in_demolab          |
	+----------------------------+
	| auth_group                 |
	| auth_group_permissions     |
	| auth_permission            |
	| auth_user                  |
	| auth_user_groups           |
	| auth_user_user_permissions |
	| demolabapp_lab             |
	| demolabapp_order           |
	| demolabapp_user            |
	| django_admin_log           |
	| django_content_type        |
	| django_session             |
	+----------------------------+
	12 rows in set (0.00 sec)
	
	mysql> exit
	Bye
	
	6. Install redis
	# http://redis.googlecode.com/files/redis-2.6.12.tar.gz
	# tar -xvf redis-2.6.14.tar.gz
	# cd redis-2.6.14
	# make
	# install
	# yum install tcl -y
	# make test
	# cd src
	# ./redis-server
	
	  405  wget https://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz --no-check-certificate
	  406  ll
	  407  tar xvf pip-1.3.1.tar.gz 
	  408  cd pip-1.3.1
	  409  ll
	  410  python setup.py install
	  411  whereis pip
	  412  pip install django-redis
	  413  whereis gcc
	  414  export PATH=/usr/bin:$PATH
	  415  export PATH=/usr/bin/gcc:$PATH
	  416  pip install django-redis
	
	
	7. Start django/redis at startup
	# mkdir /lab/script
	# cd /lab/script
	# vi django.sh
	#!/bin/sh
	/usr/bin/python /lab/demolab/manage.py runserver 192.168.1.20:80 &
	# cat redis.sh
	
	#!/bin/sh
	cd /root/redis-2.6.12/src/
	./redis-server &
	
	# vi /etc/bashrc
	sh  /lab/script/redis.sh
	sh  /lab/script/django.sh
	
	8. Install yaml
	# yum install python-yaml -y
