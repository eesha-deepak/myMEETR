# myMEETR
A web application that helps companies to organize meeting times, according to certain criteria such as importance level. Taking into account the date and time availability of each attending member for a meeting, the most suitable meeting times will be ranked in order of importance. Given our current circumstance with COVID-19, our application is aimed to help teams efficiently organize meetings time given restraints such as time zones. 

Note: If mySQLDB's module does not work for your system, copy paste the following lines into env/lib/python3.9/site-packages/click__init__.py

import pymysql
pymysql.install_as_MySQLdb()
