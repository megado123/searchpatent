import os
import sys
from os import path 

import nltk


#nltk.data.path.append('D:\home\python361x64\nltk_data')

#This file is used to download the stopwords and punkt files from NLTK.  These are required by the application and should be run 
#before using application
basedir = os.path.abspath(os.path.dirname(__file__))
nltk.data.path.clear()
nltk_path = os.path.join(basedir, 'patentsearch', 'App_Data', 'nltk_data')
nltk.data.path.append(nltk_path)
nltk.download('stopwords',download_dir = nltk_path)
nltk.download('punkt',download_dir = nltk_path)

print("downloaded to:" + nltk.data.path[0])

