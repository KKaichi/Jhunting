from apps.app import db
from flask_login import current_user

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    event_name = db.Column(db.String, index=True)
    start_day = db.Column(db.Date)
    start_time = db.Column(db.Time)
    finish_day = db.Column(db.Date)
    finish_time = db.Column(db.Time)
    memo = db.Column(db.String)


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    company_name = db.Column(db.String, index=True)

    def is_duplicate_company_name(self):
        return (
            Company.query.filter_by(user_id=current_user.id,company_name=self.company_name).first() is not None
        )
