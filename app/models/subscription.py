# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st


from app.repositories.users import UserRepository

from app import db



class Subscription(db.Model):
    id = Column(st.Integer, primary_key=True, autoincrement=True)

    subscriber = Column(st.Integer, ForeignKey('User.id'), nullable=False)
    subscribed =  Column(st.Integer, ForeignKey('User.id'), nullable=False)

    """
    @raises ValueError if subscriber_id != subscribed_id
    @returns Subscriber object, representing subscription between two users if valid
    """
    def __init__(self, subscriber_id: int, subscribed_id: int):
        
        if subscribed_id == subscriber_id:
            raise ValueError(f"Tried to subscribe user ID: {subscriber_id} to itself")
        
        subscriber = UserRepository.find_user_by_id(subscriber_id)
        subscribed = UserRepository.find_user_by_id(subscribed_id)
        #check that users exist first
        if subscriber == None:
            raise ValueError(f"Subscriber did not exist, ID: {subscriber_id}")
        if subscribed == None:
            raise ValueError(f"Subscribed user did not exist, ID: {subscribed_id}")
        
        self.subscriber = subscriber
        self.subscribed = subscribed