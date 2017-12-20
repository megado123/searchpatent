# [Search Patent](http://searchpatent.azurewebsites.net)
The [Search Patent](http://searchpatent.azurewebsites.net) application is intented to provide search functionality against the patent database hosted in Azure and made accessible through Azure Search with a Python Flask Front End with d3 extensions

The first time the application is pulled up it will take some time to load your cache - note the 1st time will take up to 1 minute.
However loading the website after the initil load will be much faster.

**Good news** 
This install is not required

*More details than required* 
Here are the instructions to install this on your computer locally.  This code has been run in both python 3.4.4 and python 3.6.1 environments

**Steps**

1.  Clone Repository

 `$ git clone https://github.com/megado123/searchpatent.git`

 2.  Install requirements.

 `> python -m pip install wheel`

Note the location of the requirements.txt file will be in your local repository - so that will need to be modifed in the example below

`> python -m pip install --upgrade -r requirements.txt`

3.  Manually run the **setup.py** file to download the nltk stopwords 


4.  Note - you don't have to run this file.  The SqlLite database is included, but it can be dropped and created through the **runserver.py** file
Running the **runserver.py** file with the argument: 'dropdb' to drop the database
Running the **runserver.py** file with the argument: 'initdb' to create the database

5.  To Run the application - set app.py as the start up file

python.exe should provide indication that application is running on http://localhost:5555

### Additional files

The project can be fun in whatever IDE is desired, but the Visual Studio Files have been included in the repository
Additional files for deployment into Azure have also been included as part of this repository
1.  web.config
2.  downloader.py (can be run in Azure environment to bring up the nltk ui)
3.  ptvs_virtualenv_proxy.py
4. .skipPythonDeployment (skip the standard deployment)
5. web.config (empty) file in the static folder



## Acknowledgements
* The HTML5 Templates used for this application initially came from [Initializr](http://www.initializr.com/)
* There is a great series on [PluralSlight](http://www.pluralsight.com) called 'Introduction to the Flask Microframework' that was served as a foundation
for building out the front end using Python, Flask, and Jinja2 Templates

## Current Deployment
* SQLLite is the database used to hold past searches and User Login in formation
* The patent database is hosted in an Azure SQL Server database 
* A view of the data was created and indexed using Azure Search
* The Python web application is hosted in Azure highlights for getting that working in the Azure platform

## Overview

## Vision
An organization that thrives on innovation, inventing a new and unique product that will be of value to the marketplace must have solid footing on existing patents.  A failure to defend itself against a patent infringement lawsuit could totally erase the profit recognized to compensate for research and development of a new product, all of which could extend over many years.
Due to the sensitive nature of the information that researchers are exploring, using Internet search tools is frequently prohibited.  Internal proprietary tools are needed. 
Our vision is to put together an application that provides relevant patent data for a researcher’s needs and interests.  The application will utilize text mining and analysis techniques to enhance the researcher’s experience.  The ultimate vision is that the researcher gains better information more quickly.

## The application is hosted at [http://searchpatent.azurewebsites.net](http://searchpatent.azurewebsites.net).   
Alternatively, the application can be downloaded at (https://github.com/megado123/searchpatent)[https://github.com/megado123/searchpatent] and installed locally.  [In either case, the application issues a call to the Azure Search API to get the results from the primary repository hosted on Azure.]

If run remotely or locally - a SQL Lite Database is used to store recent searches and user information.  When a search is requested, the Python Flask Web application uses Azure Search which has indexed patent information using IDF-TF ranking against data pulled from [http://www.patentsview.org/download/](http://www.patentsview.org/download/) and placed into a SQL Server database housed in Azure.  

The data returned from Azure Search is then used to populate a word cloud from the Titles, and gensim is used to generate LDA and HDP topic models.  In addition the top ranked companies based on patent numbers are displayed to provide a researcher immediate insight into compention/contributors to a relavent technical area.  Finally the research results are provided with a short table providing key infomration along with the abstract of a particular patent.

## Application Design
### The primary functions of the application are:
* Present form to end user for search criteria
* Provide criteria to the Azure Search API and receive results set
* Identify word tokens by frequency using the patent titles.
* Identify topics in the search results.  Latent Dirichlet Allocation (LDA) and the Hierarchical Dirichlet Allocation (HDP) methods are utilized to generate topic models and both models are displayed.
* Display results including patent meta data and patent abstract for browsing.  

### Secondary functions of the application include:
* Creation of a user account with password
* User identification and authentication 
* Maintaining a history of patent search criteria, date, time by user


### Utility functions provided include:
* Initialize local SQLLite database
* Drop and re-create local SQLLite database

### Code Structure
* The application was developed in Python with the Flask library to provide the user interactive features.  The search results are viewed in HTML frames which utilize d3 to present the data in graphical word cloud as well as HTML tables

* During the application install, a subdirectory named “searchpatent” is created.  Several application setup files are copied to that directory.  A sub-directory named “patentsearch” is also created.  Patentsearch functions as a python library and includes important library modules forms.py, views.py and models.py. 
The initiation program is app.py.

Hierarchy of major application files:
i)	Searchpatent (directory)
(1)	Requirements.txt
(2)	Setup.py
(3)	Runserver.py
(4)	App.py
(5)	Patentsearch (directory)
	(a)	Forms.py
	(b)	Views.py
	(c)	Models.py
	(d)	Templates (directory)
		(i)	Find.html
		(ii)	Results2.html
		
**__init__.py** holds configuation for flask login manager and SQLLite database

**AnotherTest.py** Simple test added to ensure NLTK library functionality from Kudu command console within the Azure Environment.

**Forms.py** contains definition of 3 class forms for user interaction: 

**home.py** was initial application start, and remained with simle functions to retrieve information from SQLLite database


| Function      | Overview      | 
| ------------- |:--------------|
| Search        | Search 	A set of search criteria fields are available to the user.  A button labeled “submit” is available once user has supplied desired criteria.|
| Login         | Login 	Fields for user ID and password are presented to user.  A button labeled “login” is available. |  
| Sign-Up       | Sign-Up	Fields for user name, email address, user ID, and 2 password are available to the user.  A button labeled “create account” is available.     | 

The classes contain information pertaining to how the input is displayed and validated on the search before submssion using wt form validators and fields 

**Views.py** contains these functions:

| Function      | Overview      | 
| ------------- |:--------------|
|Find	        |Confirm user-entered search criteria and call makerequest().  makerequest functions makes API call to Azure Search|
|Login	        |Confirm user credentials|
|Logout         |	Remove current user settings in app memory|
|Load_user	    |Get user search history|


**Models.py** contains these functions:

| Function      | Overview      | 
| ------------- |:--------------|
|Search	        |Retrieve history of searches|
|SearchFields	|Process search fields|
|SearchData	    |Initialize memory variables to process search results returned.  Call bow().  Call GetTops().|
|bow	        |Tokenize title data.  Remove stopwords, punctuation, and set lower case.  Calculate term frequency.|
|GetTops	    |Tokenize abstract text.  Remove stopwords, punctuation, and set lower case.  Call LDA model function in gensim library.  Call HDP function in gensim library.  Set up results for tabular display.|


HTML templates are utilized:

| Function      | Overview      | 
| ------------- |:--------------|
|Find.html	    |Form for user to enter search criteria and desired sort|
|Results2.html	|Form to present results to user.  Includes word cloud of frequent terms, LDA topic model, HDP topic model, and patent meta data and abstract data.|
|404.html       |When user puts in a page not found,   ex: http://searchpatent.azurewebsites.net/dog |
|505.html       |When exception occurs provides ability to send email - if they think this occured on error.|
|Base.html		|Base Template in which other templates inherit from|
|form_macro.html|Template providing ability to display field errors|
|login          |login template|
|signup         |Allows for signing up for user (recall validation is provided in forms.py|
|user           |Allows viewing past searches ex: http://searchpatent.azurewebsites.net/user/megado123 |
|index          |Welcome page for application|

### Primary Data Repository
We selected the PatentsView data source (http://patentsview.org) for patent data.  The site offers all data from 1976 to 2016 in different tables organized for a relational database.  The PatentsView website (http://www.patentsview.org/download) offers a total of 52 tables for download.  Many are reference tables to the multiple categorization codes available.  The core patent data in scope for our solution is covered in about 8 tables.  A SQL database hosted on Azure is loaded with more than 5mm patents and related data.

### Secondary Database
An additional SQLLite database is part of the application which is used to store the user logon credential data.  It also stores the search criteria submitted to date for each user.

### Search Capability
Azure offers a search function and API.   The solution designer would configure as many indices on the data as necessary.  Our application requires only one index which is a search on patent abstract data.  The search API is configured to receive an index name and search criteria fields including a sort field.  The API is called by an HTTP GET or POST.  The results set is determined by the index configuration.  Our index returns several fields including the patent title, company or organization that holds the patent, date patent granted, and location including country, state, and city.

### Team Members
Team members are Megan Masanz (mjneuman) and Cynthia Johnson (cjj4).
Megan contributed primary application architecture design and development using Python, Flask, HTML with D3.  Additionally, Azure search index configuration against primary data repository of patent data.  
Cynthia contributed research for Microsoft Azure Search, nltk and gensim libraries, and LDA and HDP topic models.  Also contributed python development for preparation and calculation of models.
Both contributed toward building repository of patent data.








