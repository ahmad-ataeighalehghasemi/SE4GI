#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 06:43:11 2019

@author: abdoul
"""

from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from psycopg2 import (
        connect
)


# Create the application instance
app = Flask(__name__, template_folder="templates",static_url_path='/static')
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_dbConn():
    if 'dbConn' not in g:
        myFile = open('dbConfig.txt')
        connStr = myFile.readline()
        g.dbConn = connect(connStr)
    
    return g.dbConn

def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT user_id FROM blog_user WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                cur.close()

        if error is None:
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO blog_user (user_name, user_password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            cur.close()
            conn.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('auth/register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_dbConn()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM blog_user WHERE user_name = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = get_dbConn()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM blog_user WHERE user_id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
    if g.user is None:
        return False
    else: 
        return True


# Create a URL route in our application for "/"
@app.route('/')
@app.route('/index')
def index():
    conn = get_dbConn()
    cur = conn.cursor()
    cur.execute(
            """SELECT blog_user.user_name, post.post_id, post.created, post.title, post.body 
               FROM blog_user, post WHERE  
                    blog_user.user_id = post.author_id"""
                    )
    posts = cur.fetchall()
    cur.close()
    conn.commit()
    load_logged_in_user()

    return render_template('blog/index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if load_logged_in_user():
        if request.method == 'POST' :
            title = request.form['title']
            body = request.form['body']
            error = None
            
            if not title :
                error = 'Title is required!'
            if error is not None :
                flash(error)
                return redirect(url_for('index'))
            else : 
                conn = get_dbConn()
                cur = conn.cursor()
                cur.execute('INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)', 
                            (title, body, g.user[0])
                            )
                cur.close()
                conn.commit()
                return redirect(url_for('index'))
        else :
            return render_template('blog/create.html')
    else :
        error = 'Only loggedin users can insert posts!'
        flash(error)
        return redirect(url_for('login'))
   
def get_post(id):
    conn = get_dbConn()
    cur = conn.cursor()
    cur.execute(
        """SELECT *
           FROM post
           WHERE post.post_id = %s""",
        (id,)
    )
    post = cur.fetchone()
    cur.close()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if post[1] != g.user[0]:
        abort(403)

    return post

@app.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if load_logged_in_user():
        post = get_post(id)
        if request.method == 'POST' :
            title = request.form['title']
            body = request.form['body']
            error = None
            
            if not title :
                error = 'Title is required!'
            if error is not None :
                flash(error)
                return redirect(url_for('index'))
            else : 
                conn = get_dbConn()
                cur = conn.cursor()
                cur.execute('UPDATE post SET title = %s, body = %s'
                               'WHERE post_id = %s', 
                               (title, body, id)
                               )
                cur.close()
                conn.commit()
                return redirect(url_for('index'))
        else :
            return render_template('blog/update.html', post=post)
    else :
        error = 'Only loggedin users can insert posts!'
        flash(error)
        return redirect(url_for('login'))

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_dbConn()                
    cur = conn.cursor()
    cur.execute('DELETE FROM post WHERE post_id = %s', (id,))
    conn.commit()
    return redirect(url_for('index'))



@app.route('/barplot', methods=('GET', 'POST'))
def barplot():
    return render_template('graphs/circonf_barplot.html')

@app.route('/cond', methods=('GET', 'POST'))
def cond():
    return render_template('graphs/Condition_tree.html')

@app.route('/number', methods=('GET', 'POST'))
def number():
    return render_template('graphs/Number_tree.html')

@app.route('/carto', methods=('GET', 'POST'))
def carto():
    return render_template('graphs/carto.html')


@app.route('/interactive_map')
def interactive_map():
    if load_logged_in_user():
        return render_template('interactive_map.html')
    else:
        error = 'Only logged in users can visualize this page!'
        flash(error)
        return redirect(url_for('login'))

@app.route('/insert_data', methods=('GET', 'POST'))
def insert_data():
    if load_logged_in_user():
        if request.method == 'POST':
            
            title = request.form['title']
            circumference = request.form['circumference']
            lat = request.form['latitude']
            lon = request.form['longitude']
            typ = request.form['type']
            condition = request.form['condition']

            
            error = None
            
            if not title:
                error = 'Name of the title is required!'
            elif (float(circumference)<0 or float(circumference) >500):
                error = 'Please insert a valid value for circumference!'
            elif (float(lat)<30.0080 or float(lat)>(50.0000)):
                error = 'Sorry but the value of the latitude is not allowed!'
            if error is not None :
                flash(error)
                return redirect(url_for('insert_data'))
            if not typ:
                error = 'Name of the type of species is required!'
            if not condition:
                error='Condition is required'
            else : 
                conn = connect("dbname=postgres user=postgres password=Kassim123*")
                cur = conn.cursor()
                cur.execute('INSERT INTO tress (title, circumference, latitude, longitude, type, condition ) VALUES (%s, %s, %s, %s, %s, %s)', 
                            (title, circumference, lat, lon, typ, condition)
                            )
                cur.close()
                conn.commit()
                return redirect(url_for('blog/index.html'))
        else :
            return render_template('insert_data.html')
    else :
        error = 'Only logged in users can insert data!'
        flash(error)
        return redirect(url_for('auth/login.html'))



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run()