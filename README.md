## Minimum system requirements
Set up on Ubuntu >= 14.10
Earlier releases do not have certain r-libraries (e.g. r-cran-matrixstats) in
apt-get

## Installation

## Install requirements
```
sudo apt-get update

sudo apt-get -y install git python-dev python-pip libffi-dev python-gdal python-numpy python-scipy python-matplotlib python-skimage python-imaging-tk ipython ipython-notebook python-pandas python-sympy python-nose python-rpy2 r-base r-base-dev r-cran-matrixstats libmysqlclient-dev mysql-server libtiff5 xvfb

sudo pip install google-api-python-client pyCrypto MySQL-python earthengine-api images2gif libtiff 

sudo mysql_secure_installation 

sudo mysql_install_db
```

If apt-get package for R is not available (e.g. I could not find the 'fields' package and its dependencies, 'spam', 'maps'), the R packages can be installed from command line. Download the following packages (e.g. use install.packages('fda') from the R shell):

_spam_, _maps_, _fields_, _fda_, _RJSONIO, _rPython_

Then build and install, if the install did not complete from the R command line:
```
sudo R CMD INSTALL --build spam_1.3-0.tar.gz
sudo R CMD INSTALL --build maps_3.1.1.tar.gz 
sudo R CMD INSTALL --build fields_8.4-1.tar.gz
sudo R CMD INSTALL --build fda_2.4.4.tar.gz
sudo R CMD INSTALL --build RJSONIO_1.3-0.tar.gz
sudo R CMD INSTALL --build rPython_0.0-6.tar.gz
```

**NOTE: ee library uses an outdated version of oauth2client (and a deprecated
function). See issue: https://github.com/google/earthengine-api/issues/5
To support this, it was necessary to uninstall oauth2client and reinstall
version 1.5.2

```
>sudo pip uninstall oauth2client
>sudo pip install oauth2client==1.5.2
```

## Set up database
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

Convert Google Earth private key to .pem
-----------------

openssl pkcs12 -nodes -nocerts -in GoogleKey.p12 -out GoogleKey.pem

if prompted for a password use: _notasecret_

(See https://developers.google.com/earth-engine/app_engine_intro)


Run pipeline
-----------------
```>xvfb-run python main.py
```

Individual functions can be run from ipython
-----------------
```>xvfb-run ipython
```
