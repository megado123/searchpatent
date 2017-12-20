from datetime import datetime
from logging import DEBUG
import os
from flask import Flask, render_template, redirect, url_for, flash
from patentsearch.forms import SearchForm

app = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'C\x01\x92P\t \xf2\xa2\x9aS\x80\xf3\xc6\xb33V9\xa2\xae\xb2\xe8_\x83\xf1'

searches = []

#stores search information into SQLLite database
def store_search(searchtext):
    searches.append(dict(
        searchtext = searchtext,
        user = "test",
        date = datetime.utcnow()
    ))

#returns the recent searches for displaying on the welcome screen
def new_searches(num):
    return sorted(searches, key=lambda ps: ps['date'], reverse=True)[:num]

#returns html for display
def new_table(html):
    return html

