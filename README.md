# [Search Patent](http://searchpatent.azurewebsites.net)
The [Search Patent](http://searchpatent.azurewebsites.net) application is intented to provide search functionality against the patent database hosted in Azure and made accessible through Azure Search with a Python Flask Front End with d3 extensions

**Good news** This install is not required

*More details than required* 
Here are the instructions to install this on your computer locally.  This code has been run in both python 3.4.4 and python 3.6.1 environments

**Steps**

1.  Clone Repository

 `$ git clone https://github.com/megado123/searchpatent.git`

 2.  Install requirements.

 `> C:\Python34\python.exe -m pip install wheel`

Note the location of the requirements.txt file will be in your local repository - so that will need to be modifed in the example below

`> C:\Python34\python.exe -m pip install --upgrade -r requirements.txt`

3.  Manually run the **setup.py** file to download the nltk stopwords 

4.  The SqlLite database is included, but it can be dropped and created throug the **runserver.py** file
Running the **runserver.py** file with the argument: 'dropdb' to drop the database
Running the **runserver.py** file with the argument: 'initdb' to create the database

### Additional files

The project can be fun in whatever IDE is desired, but the Visual Studio Files have been included in the repository
Additional files for deployment into Azure have also been included as part of this repository
1.  web.config
2.  downloader.py (can be run in Azure environment to bring up the nltk ui)
3.  ptvs_virtualenv_proxy.py
4. .skipPythonDeployment (skip the standard deployment)
5. web.config (empty) file in the static folder
6. patentsearch.sln (for viewing with Visual Studio)
7. patentsearch.pyproj.user (for viewing with Visual Studio)
8. patentsearch.pyproj (for viewing with Visual Studio)


## Acknowledgements
* The HTML5 Templates used for this application initially came from [Initializr](http://www.initializr.com/)
* There is a great series on [PluralSlight](http://www.pluralsight.com) called 'Introduction to the Flask Microframework' that was served as a foundation
for building out the front end using Python, Flask, and Jinja2 Templates

## Current Deployment
* SQLLite is the database used to hold past searches and User Login in formation
* The patent database is hosted in an Azure SQL Server database 
* A view of the data was created and indexed using Azure Search
* The Python web application is hosted in Azure highlights for getting that working in the Azure platform


