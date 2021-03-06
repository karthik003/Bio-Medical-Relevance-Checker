from project import app,db
from flask import render_template,redirect,request,url_for,flash,abort
from flask_login import login_user,login_required,logout_user
from project.models import User,UserSearch
from project.forms import LoginForm, RegistrationForm,SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
from main import *
import os
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))


@app.route('/login',methods=['GET','POST'])
def login():

    form= LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in Successfully!')
            return redirect(url_for('search'))
        
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()

    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')

        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route('/search',methods=['GET','POST'])    
def search():
    form=SearchForm()
    if form.validate_on_submit():
        user=UserSearch(search=form.search.data,userid=form.userid.data)
        search=form.search.data
        userid=form.userid.data
        db.session.add(user)
        db.session.commit()
        relevance(search)
        return '''<h1>The User id is {}<h1>
                  <h1>The Query searched is {}<h1>
                  <h1 style="text-align:center">The most relevant links are : -</h1>
                '''.format(userid,search)
                  

    return render_template('searchbar.html',form=form)    

if __name__=='__main__':
    app.run(debug=True)
