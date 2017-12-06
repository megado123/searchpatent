# patentsearch
This application is intented to provide search functionality against the patent database hosted in Azure and made accessible through Azure Search

0.  install requirements - the requirements.txt file has all the required stuff, except...

1.  had to manuall run the **downloader.py** (this will get the additional nltk stuff)

2.  had to manually run the **runserver.py** to delete and then create the sqllite database so it would
associate properly.

## Acknowledgements
* The HTML5 Templates used for this application initially came from [Initializr](http://www.initializr.com/)
* There is a great series on [PluralSlight](www.pluralsight.com) called 'Introduction to the Flask Microframework' that was served as a foundation
for building out the front end using Python, Flask, and Jinja2 Templates

## Current Deployment
* SQLLite is the database used to hold past searches and User Login in formation
* The patent database is hosted in an Azure SQL Server database 
* A view of the data was created and indexed using Azure Search
* The Python web application is hosted in Azure highlights for getting that working in the Azure platform:
1.	Changed webconfig point to 3.6 per the url link you provide
2.	Changed requirents.txt per the url link you provided
3.	Include a .skipDeployment script
4.	Did -m pip install wheel
5.	Did -m pip install –upgrade -r requirements.txt
6.	Run my downloader.py file to get nltk stuff



