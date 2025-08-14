from app.models import Night

def last_seven_nights():
    nights_slice = Night.query.order_by(Night.day.desc()).limit(7).all()
    reversed_slice = nights_slice[::-1] # put the dates back in ascending order
    return dict(
        sleep = [dict(x=n.day.isoformat(), y=n.amount.total_seconds()/3600) for n in reversed_slice],
        in_bed = [dict(x=n.day.isoformat(), y=(n.to_rise - n.to_bed).total_seconds()/3600) for n in reversed_slice]
    )
def avg_sleep_all_time():
    # per year:
    # select strftime('%Y', day) as year, avg(strftime('%s', amount)) / 3600 as avg_sleep_hours from nights group by strftime('%Y', day);
    # Good luck with translating that to sqlalchemy ORM
    return []
