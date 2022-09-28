from apps.app import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    company_id = db.Column(db.String, db.ForeinKey("companies.id"))
    event_name = db.Column(db.String, index=True)
    start_day = db.Column(db.Date)
    start_time = db.Column(db.Time)
    start_day = db.Column(db.Date)
    start_time = db.Column(db.Time)
    memo = db.Column(db.String)


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    company_name = db.Column(db.String, index=True)
