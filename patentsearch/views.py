from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, login_user, current_user, logout_user
from patentsearch import app, db, login_manager
from patentsearch.forms import SearchForm, LoginForm, SignupForm
from patentsearch.models  import  User, Search, SearchData, SearchFields
from urllib.request import urlretrieve
from urllib.parse import quote
import httplib2
import json
import requests
import pandas as pd


indexName = 'azuresql-index'
serviceName = 'searchpatent'
apiversion =  '2016-09-01'
apiKey = 'F8BE68AEC4CBA8BB7A6F7BBDE6543E2B'


#method used to make GET API call to Azure Search returning data from API call
def makerequest(searchObject):
    pd.set_option('display.max_colwidth', -1)
    substring = ''
    filter = ''
    #these are the filters provided on the site - Azure has 2 core functionalities in Azure Search
    #search and filter, these parameters are used for filteing
    if len(searchObject.country)>0:
        filter = filter + "country eq '" + searchObject.country + "'"

    if len(searchObject.patentnumber)>0:
        if len(substring) > 0:
            filter = filter + "&id eq '" + quote(searchObject.patentnumber)+ "'"
        else:
            filter = filter + "id eq '" + quote(searchObject.patentnumber)+ "'"
    if len(searchObject.organization)>0:
        if len(substring) > 0:
            filter = filter + "&organization eq '" + quote(searchObject.organization) + "'"
        else:
            filter = filter + "organization eq '" + quote(searchObject.organization) + "'"
    if len(searchObject.kind)>0:
        if len(substring) > 0:
            filter = filter + "&kind eq '" + quote(searchObject.kind) + "'"
        else:
            filter = filter + "kind eq '" + quote(searchObject.kind) + "'"

    if (len(searchObject.searchtext) > 0 and len(filter) > 0 ):
        substring = substring + 'abstract:' + quote(searchObject.searchtext)

    if len(substring) == 0:
        substring = quote(searchObject.searchtext)

    if len(substring) > 0:
        substring = '&search=' + substring + '&queryType=full'
    if len(filter) > 0:
        substring = substring + '&$filter=' + filter

    #not searching on any specific field
    if len(substring) == 0:
        if len(searchObject.searchtext)==0:
            substring = '&search=*'

    #this is basic functionality to enable skip and take
    skipString = ''
    if (searchObject.skip != None ):
        skipString = '&%24skip=' + str(searchObject.skip)

    recordnumberString = '&%24top=' + searchObject.recordnumber

    url = 'https://' + serviceName + '.search.windows.net/indexes/' + indexName + '/docs?api-version=' + apiversion + substring +  '&api-key=' + apiKey + '&facet=organization'  + skipString + recordnumberString
    if (searchObject.sortby == 'date' ):
        url = url + '&%24orderby=date%20desc'
    r = requests.get(url)
    data = r.json()

    return data


#get user based on user id from SQL Lite DB
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

#routes to welcome screen
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_searches=Search.newest(5))

#routes to a specific user 
@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

#This is the landing page for the search. When the form is submitted, a POST the search is added to the db, and an API call is made to Azure
@app.route('/find', methods=['GET', 'POST'])
@login_required
def find():
    form = SearchForm()
    if form.is_submitted():
        searchtext = form.searchtext.data
        country = form.country.data
        author = ''
        patentnumber = form.patentnumber.data
        organization = form.organization.data
        cpcs = form.cpcs.data
        sortby = form.sortby.data
        skip = form.skip.data
        recordnumber = form.recordnumber.data
        
		#save search in db
        bm = Search(searchtext=searchtext, user=current_user, country=country, author=author, patentnumber=patentnumber, organization=organization, cpcs=cpcs)
        db.session.add(bm)
        db.session.commit()

		#populate a class for easy transfer of information
        searchAgainst = SearchFields(searchtext = searchtext, country = country, organization = organization, kind = cpcs, patentnumber = patentnumber, sortby = sortby, skip = skip, recordnumber = recordnumber)
		#make API call and return data
        data = makerequest(searchAgainst)

		#the Company and the number of patents is returned in the facet for displaying top ranked companies and the number of patents
        orgs = data['@search.facets']['organization']
		#the faceted information is removed from the data
        data = data['value']
        
		#check if no results are found in the case of searching jsdkflsjdfjksdlf no results will be found, this handles that case
        if (len(data) == 0):
            s = 'no results'
            flash('No results found, please try another search')
            return render_template('find.html', form=form)

        s = ''
        for item in data:
            s = item['title'] + " " + s

        searchData = SearchData(s, jsonData= data, orgs = orgs)
        
        return render_template(('results2.html'), table=searchData)
      

    return render_template('find.html', form=form)


#routing to the login screen
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
 
            login_user(user, remember = form.remember_me, force = True)
            flash("Logged in as  {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user',
                                                username=user.username))
        flash('Incorrect username or password.')
    else:
        
        form.username.data = 'createUser'
        form.username.data = ''
        form.password.data = ''

    return render_template("login.html", form=form)

#routing to the logout screen
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

#routing to allow users to sign up and be added to db
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {} Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

#handling 404 issues
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#handling 500 errors - hopefully there are none.
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
