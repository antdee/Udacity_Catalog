#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Room, Base, Product, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "My Udacity Catalog App"

# Connect to Database and create database session
engine = create_engine('postgresql://catalog:catalog@localhost/furniture')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Implementing login with Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.12/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull outtheactual token value and replace the
        remaining quotes with nothing so that it can be useddirectly in the
        graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.12/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.12/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px;
                             height: 300px;
                             border-radius: 150px;
                             -webkit-border-radius: 150px;
                             -moz-border-radius: 150px;"> '''

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
            facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Implementing login with Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    print 'gcon'
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
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
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
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
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

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius:
                    150px;-webkit-border-radius: 150px;-moz-border-radius:
                    150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

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
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showRooms'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showRooms'))


# JSON APIs
@app.route('/users/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(users=[u.serialize for u in users])


@app.route('/allrooms/JSON/')
def roomsJSON():
    rooms = session.query(Room).all()
    return jsonify(rooms=[r.serialize for r in rooms])


@app.route('/allproducts/JSON/')
def allProductsJSON():
    products = session.query(Product).all()
    return jsonify(products=[r.serialize for r in products])


@app.route('/<room_name>/JSON/')
def roomProductsJSON(room_name):
    products = session.query(Product).filter_by(room=room_name).all()
    return jsonify(room_products=[r.serialize for r in products])


# Rooms and Products pages
@app.route('/')
@app.route('/shop/')
def showRooms():
    rooms = session.query(Room).order_by(asc(Room.name))
    return render_template('shop.html', rooms=rooms,
                           login_session=login_session)


@app.route('/shop/<room_name>/')
@app.route('/shop/<room_name>/products/')
def showProducts(room_name):
    room = session.query(Room).filter_by(name=room_name).one()
    products = session.query(Product).filter_by(room=room_name).all()
    return render_template('products.html', products=products, room=room,
                           login_session=login_session)


@app.route('/shop/new/', methods=['GET', 'POST'])
def newProduct():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newProduct = Product(name=request.form['name'],
                             description=request.form['description'],
                             price=request.form['price'],
                             image=request.form['image'],
                             room=request.form['room'],
                             user_id=login_session['user_id'],
                             user_picture=login_session['picture'])
        room = request.form['room']
        session.add(newProduct)
        flash('New Product Added \n %s' % newProduct.name)
        session.commit()
        return redirect(url_for('showProducts', room_name=room))
    else:
        return render_template('newproduct.html', login_session=login_session)


@app.route('/shop/<int:product_id>/edit/', methods=['GET', 'POST'])
def editProduct(product_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToEdit = session.query(Product).filter_by(id=product_id).one()
    if itemToEdit.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not authorized
                to edit this product. Please list your own product in order to
                edit.');}</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['price']:
            itemToEdit.price = request.form['price']
        if request.form['image']:
            itemToEdit.image = request.form['image']
        if request.form['room']:
            itemToEdit.room = request.form['room']
        session.add(itemToEdit)
        flash('Item Edited \n %s' % itemToEdit.name)
        session.commit()
        return redirect(url_for('showProducts', room_name=itemToEdit.room))
    else:
        return render_template('editproduct.html', itemToEdit=itemToEdit,
                               login_session=login_session)


@app.route('/shop/<int:product_id>/delete/', methods=['GET', 'POST'])
def deleteProduct(product_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Product).filter_by(id=product_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not authorized
                 to delete this product. Please list your own product in
                 order to delete.');}</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('Item Deleted \n %s' % itemToDelete.name)
        session.commit()
        return redirect(url_for('showProducts', room_name=itemToDelete.room))
    else:
        return render_template('deleteproduct.html', itemToDelete=itemToDelete,
                               login_session=login_session)


@app.route('/profiles/<int:user_id>')
def showProfile(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    products = session.query(Product).filter_by(user_id=user_id).all()
    return render_template('profile.html', user=user,
                           products=products, login_session=login_session)


@app.route('/buy/<int:product_id>')
def buyProduct(product_id):
    product = session.query(Product).filter_by(id=product_id).one()
    user = session.query(User).filter_by(id=product.user_id).one()
    return render_template('buyproduct.html', product=product,
                           user=user, login_session=login_session)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
