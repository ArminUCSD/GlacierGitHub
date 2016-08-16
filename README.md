#Installation

#Install requirements
```
sudo apt-get update

sudo apt-get -y install git python-dev python-pip python-gdal python-numpy python-scipy python-matplotlib python-skimage python-imaging-tk ipython ipython-notebook python-pandas python-sympy python-nose python-rpy2 r-base libmysqlclient-dev mysql-server libtiff5

sudo pip install google-api-python-client pyCrypto earthengine-api images2gif libtiff 

sudo mysql_secure_installation 

sudo mysql_install_db
```

#Set up database
Set mysql root password. Default user for this application is 'root'. See ```Docs/``` for details. To set root password, see http://dev.mysql.com/doc/refman/5.7/en/default-privileges.html

Create 'glaciers' database
------------------
```
> mysql -u root -p[root_password]
> CREATE DATABASE glaciers;
```


Restore database from sqldump.sql
------------------

```> mysql -u root -p[root_password] glaciers < sqldump.sql```
