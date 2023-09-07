import pendulum

from flask_login import login_user, logout_user, login_required

from app import app, db, login_manager, bcrypt
from flask import render_template, redirect, url_for, request, abort, flash

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
@login_required
def homepage():
    nights = Night.query.order_by(Night.day).all()
    nb = len(nights)
    if nb == 0:
        return render_template('index.html', nb_nights=nb, today=pendulum.today())

    first = nights[0].day
    last = nights[-1].day
    nbmissing = nb - (last - first).days - 1
    return render_template('index.html', nb_nights=nb, today=pendulum.today().date(), first_date=first, last_date=last, nbmissing=nbmissing)


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


@app.route('/places/', methods=['GET'])
@login_required
def show_places():
    placelist = Place.query.all()
    return render_template('places-home.html', places=placelist)


@app.route('/places/new', methods=['GET', 'POST'])
@login_required
def add_place():
    form = PlaceForm()
    
    if form.validate_on_submit():
        place = Place(name=form.name.data, lat=form.latitude.data, lon=form.longitude.data)
        # form.populate_obj(place)
        db.session.add(place)
        db.session.commit()
        return redirect(url_for('show_places'))
    
    return render_template('place-form.html', form=form)


@app.route('/places/<int:pid>', methods=['GET', 'POST'])
@login_required
def place(pid):
    place = Place.query.get_or_404(pid)
    form = PlaceForm()

    if form.validate_on_submit():
        place.update(name=form.name.data, lat=form.latitude.data, lon=form.longitude.data)
        # form.populate_obj(place)
        db.session.commit()
        return redirect(url_for('show_places'))

    form.name.data = place.name
    form.latitude.data = place.latitude
    form.longitude.data = place.longitude

    return render_template('place-form.html', form=form)


@app.route('/places/archive/<int:pid>')
@login_required
def archive_place(pid):
    """
    Toggle the place's archived status.
    """
    p = Place.query.get_or_404(pid)

    p.archived = not p.archived
    db.session.commit()

    return redirect(url_for('show_places'))


@app.route('/places/delete/<int:pid>')
@login_required
def delete_place(pid):
    p = Place.query.get_or_404(pid)

    if len(p.nights) == 0:
        db.session.delete(p)
        db.session.commit()
        flash('Suppression de %s effectuée.' % p.name)
    else:
        # abort because we are not deleting a place already linked to nights
        flash('Suppression de %s echouée (en relation avec %d nuits).' % (p.name, len(p.nights)))

    return redirect(url_for('show_places'))


@app.route('/nights/', methods=['GET'])
@login_required
def show_nights():
    date = pendulum.today()
    date_list = [date]
    for _ in range(7):
        date = date.subtract(days=1)
        date_list.append(date)

    return render_template('nights-home.html', dates=date_list)


@app.route('/nights/<date:date>', methods=['GET', 'POST'])
@login_required
def night(date):
    """
    Create a night, or edit it if it already exists
    """
    night = Night.from_date(date)

    form = NightForm()
    form.day.data = date

    if form.validate_on_submit():
        print('form date : {}'.format(form.day.data))
        # populate night with form data
        is_new_night = night is None

        if is_new_night:
            night = Night()

        form.populate_obj(night)

        night.to_bed = form.to_bed_datetime()
        night.to_rise = form.to_rise_datetime()

        if is_new_night:
            db.session.add(night)
            print('new night', night)
        else:
            print('updated night', night)

        db.session.commit()
        return redirect(url_for('night', date=date))

    previousd = date.subtract(days=1)
    nextd = date.add(days=1)

    if night is not None:
        # populate form with night data
        form.to_bed.data = night.to_bed.time()
        form.to_rise.data = night.to_rise.time()
        form.amount.data = night.amount
        form.place.data = night.place
        form.alone.data = night.alone
        form.sleepless.data = night.sleepless

    return render_template('night-form.html', form=form, date=date, previous=previousd, next=nextd)
