#Importing Flask...
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasetup import Base, User, Category, CategoryList, Items
#Importing Flask Name Function... 
app = Flask(__name__)


#Imports for Authentication
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


#To get Client Id from json file...
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

#Connect to database and create database session...
engine = create_engine('sqlite:///Catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()




# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #See if User exists...
    user_id = getUserID(login_session)
    if not user_id:
    	user_id = CreateUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
     #   del login_session['access_token']
     #   del login_session['gplus_id']
     #   del login_session['username']
     #   del login_session['email']
     #   del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
	if 'provider' in login_session:
		if login_session['provider'] =='google':
			gdisconnect()
			del login_session['gplus_id']
			del login_session['access_token']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		flash("You have successfully been logged out.")
		session.rollback()
		return redirect(url_for('showLogin'))
	else:
		flash("You were not logged in to begin with!")
		return redirect(url_for('showLogin'))




# User Helper function...
def CreateUser(login_session):
	newUser = User(name=login_session['username'] , email=login_session['email'] , picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	return newUser.id

def getUSerInfo(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	return user

def getUserID(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None



#To get data from api's in serailizable form...
@app.route('/catalog/categories/JSON')
def categoriesJSON():
	categories = session.query(Category).all()
	return jsonify(Category = [category.serialize for category in categories])


@app.route('/catalog/categories/<int:category_id>/list/JSON')
def categoryListJSON(category_id):
	List = session.query(CategoryList).filter_by(category_id = category_id).all()
	return jsonify(CategoryList = [item.serialize for item in List])


@app.route('/catalog/categories/<int:category_id>/list/<int:list_id>/JSON')
def listChoiceJSON(category_id , list_id):
	ListItem = session.query(Items).filter_by(id = list_id).all()
	return jsonify(Items = [item.serialize for item in ListItem])

@app.route('/catalog/categories/<int:category_id>/list/<int:list_id>/items/<int:item_id>/JSON')
def listChoiceItemJSON(category_id, list_id, item_id):
	Item = session.query(Items).filter_by(id = item_id).one()
	return jsonify(Items = Item.serialize)



#All Categories...
@app.route('/catalog')
def showCategory():
	categories = session.query(Category).all()
	if 'username' not in login_session:
		return render_template('publicCategory.html' , categories = categories)
	else:
		return render_template('showCategory.html' , categories = categories)


#Add New Category...
@app.route('/catalog/new' , methods = ['GET' , 'POST'])
def newCategory():
	#return "This page will be for making a new category..."
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		new_category = Category(name = request.form['name'])
		session.add(new_category)
		session.commit()
		flash("New Category %s Successfully Added" % new_category.name)
		return redirect(url_for('showCategory'))
	else:
		return render_template('newCategory.html')

#Edit an Existing Category Page...
@app.route('/catalog/<int:category_id>/edit' , methods = ['GET' , 'POST'])
def editCategory(category_id):
	#return "This page will be for editing existing categories..."
	editedCategory = session.query(Category).filter_by(id = category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedCategory.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this category. Please create your own category in order to edit.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name = request.form['name']
		session.add(editedCategory)
		session.commit()
		flash("Category Successfully Edited")
		return redirect(url_for('showCategory'))
	else:
		return render_template('editCategory.html' , i = editedCategory)

#Delete an Existing Category Page...
@app.route('/catalog/<int:category_id>/delete' , methods =['GET' , 'POST'])
def deleteCategory(category_id):
	#return "This page will be for deleting an existing category"
	deletedCategory = session.query(Category).filter_by(id = category_id).one()
	items = session.query(CategoryList).filter_by(category_id = category_id).all()
	if 'username' not in login_session:
		return redirect('/login')
	if deletedCategory.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own category in order to delete.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(deletedCategory)
		session.commit()
		flash("Category Successfully Deleted")
		return redirect(url_for('showCategory'))
	else:
		return render_template('deleteCategory.html' , i = deletedCategory , items = items)



#Provides List of Choices available in given Category...
@app.route('/catalog/<int:category_id>/list')
def showCategoryList(category_id):
	category = session.query(Category).filter_by(id = category_id).one()
	categorylist = session.query(CategoryList).filter_by(category_id = category_id).all()
	creator = getUSerInfo(category.user_id)
	if 'username' not in login_session:
		return render_template('publicCategoryList.html' , list = categorylist, category = category, creator= creator)
	else:
		return render_template('showCategoryList.html' , list = categorylist, category = category, creator=creator)



#Add New Choice to the Category list Page...
@app.route('/catalog/<int:category_id>/list/new' , methods = ['GET' , 'POST'])
def newToCategoryList(category_id):
	#return "This page will be for making a new choice for catagorylist..."
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newCategoryList = CategoryList(name = request.form['name'])
		session.add(newCategoryList)
		session.commit()
		flash("New Choice %s Successfully Created" % newCategoryList.name)
		return redirect(url_for('newListItem' , category_id = category_id, list_id = newCategoryList.id))
	else:
		return render_template('newToCategoryList.html')

#Edit an Existing Choice Page...
@app.route('/catalog/<int:category_id>/list/<int:list_id>/edit' , methods = ['GET' , 'POST'])
def editCategoryList(category_id, list_id):
	#return "This page will be for editing existing Choice in category list..."
	categoryList = session.query(Category).filter_by(id = category_id).one()
	editedChoice = session.query(CategoryList).filter_by(id = list_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedChoice.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this choice. Please create your own category in order to edit choices.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['name']:
			editedChoice.name = request.form['name']
		session.add(editedChoice)
		session.commit()
		flash("Category List Successfully Edited")
		return redirect(url_for('showCategoryList' , category_id = category_id))
	else:
		return render_template('editCategoryList.html' , i = editedChoice, category = categoryList)

#Delete an Existing Choice Page...
@app.route('/catalog/<int:category_id>/list/<int:list_id>/delete' , methods =['GET' , 'POST'])
def deleteFromCategoryList(category_id, list_id):
	#return "This page will be for deleting ran existing choice in category list"
	categoryList = session.query(CategoryList).filter_by(category_id = category_id).all()
	deletedChoice = session.query(CategoryList).filter_by(id = list_id).one()
	Item = session.query(Items).filter_by(id = list_id).all()
	if 'username' not in login_session:
		return redirect('/login')
	if deletedChoice.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete this choice. Please create your own category in order to edit choices.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(deletedChoice)
		session.commit()
		flash("Selected Choice Successfully Deleted")
		return redirect(url_for('showCategoryList' , category_id = category_id))
	else:
		return render_template('deleteFromCategoryList.html' , i = deletedChoice , items = Item, category_id = category_id)


#To show all items in particular choice of certain category....
@app.route('/catalog/<int:category_id>/list/<int:list_id>' , methods = ['GET' , 'POST'])
@app.route('/catalog/<int:category_id>/list/<int:list_id>/items' , methods = ['GET' , 'POST'])
def showListItems(category_id, list_id):
	#return "This page is for showing all items in particular choice of certain category"
	choice = session.query(CategoryList).filter_by(id = list_id).one()
	Item = session.query(Items).filter_by(id = list_id).all()
	creator = getUSerInfo(choice.user_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicListItems.html' , choice = choice , Item = Item , creator = creator)
	else:
		return render_template('showListItems.html' , choice = choice, Item = Item, creator = creator)
#Add a New Item to list of partecular choice of certain category...
@app.route('/catalog/<int:category_id>/list/<int:list_id>/items/new' , methods = ['GET' , 'POST'])
def newListItem(category_id, list_id):
	#return "This page is for Adding a New Item to list of particular choice of certain category"
	if 'username' not in login_session:
		return redirect('/login')
	choice = session.query(CategoryList).filter_by(id = category_id).one()
	if login_session['user_id'] != choice.user_id:
		return "<script>function myFunction() {alert('You are not authorized to add  items to this list.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		newItem = Items(name = request.form['name'] , price = request.form['price'] , description = request.form['description'] , list_id = list_id)
		session.add(newItem)
		session.commit()
		flash('List Item Created')
		return redirect(url_for('showListItems' , list_id = list_id, category_id = category_id))
	else:
		return render_template('newListItem.html' , list_id = list_id, category_id = category_id)
#Edit an Existing Item to list of particular choice of certain category...
@app.route('/catalog/<int:category_id>/list/<int:list_id>/items/<int:item_id>/edit' , methods = ['GET' , 'POST'])
def editListItem(category_id, list_id, item_id):
	#return "This page is for editing menu item"
	choice = session.query(CategoryList).filter_by(id = list_id).all()
	editedItem = session.query(Items).filter_by(id = item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if choice.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit items to this list.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['price']:
			editedItem.price = request.form['price'] 
		if request.form['description']:
			editedItem.description = request.form['description'] 
		editedItem.list = choice
		editedItem.id = item_id
		session.add(editedItem)
		session.commit()
		flash("List Item Successfully Edited")
		return redirect(url_for('showListItems' , list_id = list_id, category_id = category_id))
	else:
		return render_template('editListItem.html' , i = editedItem , choice = choice)
#Delete an Existing Item to list of particular choice of certain category...
@app.route('/catalog/<int:category_id>/list/<int:list_id>/items/<int:item_id>/delete' , methods = ['GET' , 'POST'])
def deleteListItem(category_id, list_id, item_id):
	#return "This page is for deleting item of list of particular choice of certain category"
	choice = session.query(CategoryList).filter_by(id = list_id).one()
	deletedItem = session.query(Items).filter_by(id = item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if deletedItem.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete items of this list.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("List Item Successfully Deleted")
		return redirect(url_for('showListItems' , list_id = list_id, category_id = category_id))
	else:
		return render_template('deleteListItem.html' , i = deletedItem , choice = choice)

if __name__ == '__main__':
	app.secret_key = "no_secret_key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)