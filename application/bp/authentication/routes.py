from flask import render_template, redirect, url_for, flash, current_app
from application.database import db
from application.models import User
from application.bp.authentication.forms import RegistrationForm
from application.bp.authentication import authentication

@authentication.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@authentication.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Form validation includes duplicate email check
        user = User.create(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('authentication.dashboard'))
    
    return render_template('registration.html', form=form)