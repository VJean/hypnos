import datetime

from flask_login import login_user, logout_user, login_required

from app import app, db, login_manager, bcrypt
from flask import render_template, redirect, url_for, request, abort

from app.forms import NightForm, PlaceForm, LoginForm
from app.models import Night, Place, User
from app.util import is_safe_url

login_manager.login_view = 'login'
db.create_all()

# if no user found, create admin from config
if User.nb_users() == 0:
    u = app.config['ADMIN_USER']
    p = app.config['ADMIN_PASSWORD']
    User.create(u, p)


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                next = request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                if not is_safe_url(next):
                    return abort(400)
                return redirect(next or url_for('homepage'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/places', methods=['GET', 'POST'])
@login_required
def show_places():
    form = PlaceForm()
    if form.validate_on_submit():
        place = Place()
        form.populate_obj(place)
        db.session.add(place)
        db.session.commit()
        return redirect(url_for('show_places'))

    return render_template('places2.html', form=form)


@app.route('/nights', methods=['GET', 'POST'])
@login_required
def show_nights():
    form = NightForm()
    places = []
    for p in Place.query.all():
        places.append((p.id, p.name))
    form.place.choices = places
    last_night = Night.get_last_night()
    nextdate = datetime.date.today()
    if last_night is None:
        pass
    else:
        nextdate = last_night.day + datetime.timedelta(days=1)
    if form.validate_on_submit():
        new_night = Night()
        form.populate_obj(new_night)

        new_night.to_bed = form.to_bed_datetime()
        new_night.to_rise = form.to_rise_datetime()
        new_night.place = Place.query.get(form.place.data)

        db.session.add(new_night)
        db.session.commit()
        print('new night', new_night)
        return redirect(url_for('show_nights'))
    return render_template('nights2.html', form=form, datestr=nextdate.strftime("%d/%m/%Y"), last_night=last_night)
