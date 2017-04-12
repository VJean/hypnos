from app import app, db
from flask import render_template, redirect, url_for

from app.forms import NightForm, PlaceForm
from app.models import Night, Place, User

# if no user found, create admin from config
if User.nb_users() == 0:
    u = app.config['ADMIN_USER']
    p = app.config['ADMIN_PASSWORD']
    User.create(u, p)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/places', methods=['GET', 'POST'])
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
def show_nights():
    form = NightForm()
    places = []
    for p in Place.query.all():
        places.append((p.id, p.name))
    form.place.choices = places
    if form.validate_on_submit():
        new_night = Night()
        form.populate_obj(new_night)

        new_night.to_bed = form.to_bed_datetime()
        new_night.to_rise = form.to_rise_datetime()
        new_night.place = Place.query.get(form.place.data)
        new_night.amount = form.amount_timedelta()

        db.session.add(new_night)
        db.session.commit()
        print('new night', new_night)
        return redirect(url_for('show_nights'))
    return render_template('nights2.html', form=form)
