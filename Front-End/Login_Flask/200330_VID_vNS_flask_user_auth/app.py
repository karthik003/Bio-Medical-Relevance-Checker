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
                <ul>
                <li>  <a href="https://www.webmd.com/sleep-disorders/hypersomnia">https://www.webmd.com/sleep-disorders/hypersomnia</a></li>
               <br> <li>  <a href="https://www.who.int/medical_devices/meddev_ebola/en/">https://www.who.int/medical_devices/meddev_ebola/en/</a></li>
                <br><li>  <a href="https://www.scitechnol.com/scholarly/medical-genetics-journals-articles-ppts-list.php"> https://www.scitechnol.com/scholarly/medical-genetics-journals-articles-ppts-list.php</a></li>
                <br><li>  <a href="https://www.sciencedirect.com/topics/nursing-and-health-professions/peak-inspiratory-pressure?dgcid=scitechconnect_SDtopics_biomed_beddows_peakinspiratorypressure   ">https://www.sciencedirect.com/topics/nursing-and-health-professions/peak-inspiratory-pressure?dgcid=scitechconnect_SDtopics_biomed_beddows_peakinspiratorypressure    </a></li>
                <br><li>  <a href="https://www.sciencedirect.com/topics/medicine-and-dentistry/saddle-anesthesia?dgcid=scitechconnect_SDtopics_biomed_beddows_saddleanesthesia">https://www.sciencedirect.com/topics/medicine-and-dentistry/saddle-anesthesia?dgcid=scitechconnect_SDtopics_biomed_beddows_saddleanesthesia</a></li>
                <br><li>  <a href="https://www.sciencedirect.com/topics/medicine-and-dentistry/rovsings-sign?dgcid=scitechconnect_SDtopics_biomed_beddows_rovsingssignhttps://www.sciencedirect.com/topics/medicine-and-dentistry/rovsings-sign?dgcid=scitechconnect_SDtopics_biomed_beddows_rovsingssign">https://www.sciencedirect.com/topics/medicine-and-dentistry/rovsings-sign?dgcid=scitechconnect_SDtopics_biomed_beddows_rovsingssign </a></li>
                <br><li>  <a href="https://www.sciencedirect.com/topics/medicine-and-dentistry/romanowsky-stain?dgcid=scitechconnect_SDtopics_biomed_beddows_romanowskystai">https://www.sciencedirect.com/topics/medicine-and-dentistry/romanowsky-stain?dgcid=scitechconnect_SDtopics_biomed_beddows_romanowskystai </a></li>
                <br><li>  <a href="https://www.sciencedirect.com/topics/medicine-and-dentistry/corneal-reflex?dgcid=scitechconnect_SDtopics_biomed_beddows_cornealreflex">https://www.sciencedirect.com/topics/medicine-and-dentistry/corneal-reflex?dgcid=scitechconnect_SDtopics_biomed_beddows_cornealreflex </a></li>
                <br><li>  <a href="https://www.sciencedirect.com/topics/medicine-apythonnd-dentistry/biomedical-research">https://www.sciencedirect.com/topics/medicine-and-dentistry/biomedical-research </a></li>
                <br><li>  <a href="https://www.sciencedirect.com/topics/biochemistry-genetics-and-molecular-biology/hypersegmented-neutrophil?dgcid=scitechconnect_SDtopics_biomed_beddows_hypersegmentedneutrophil">https://www.sciencedirect.com/topics/biochemistry-genetics-and-molecular-biology/hypersegmented-neutrophil?dgcid=scitechconnect_SDtopics_biomed_beddows_hypersegmentedneutrophil </a></li>
                <br><li>  <a href="https://www.mtu.edu/biomedical/department/what-is/"> https://www.mtu.edu/biomedical/department/what-is/</a></li>
                <br><li>  <a href="https://www.aboutbioscience.org/topics/biomedical-engineering/"> https://www.aboutbioscience.org/topics/biomedical-engineering/</a></li>
                <br><li>  <a href="https://en.wikipedia.org/wiki/Biomedical_engineering"> https://en.wikipedia.org/wiki/Biomedical_engineering</a></li>
                </ul>'''.format(userid,search)
                  

    return render_template('searchbar.html',form=form)    

if __name__=='__main__':
    app.run(debug=True)
