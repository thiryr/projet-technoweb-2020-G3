"""class for static methods around the Subscription table"""

from typing import List

from app import db
from app.models.subscription import Subscription
from app.repositories.users import find_user_by_id


    
def get_subscriptions_from(userid: int) -> List[Subscription]:
    """
    Returns a list of subscription from that user id or None
    """
    return Subscription.query.filter_by(subscriber=userid).all()

def get_subscriptions_to(userid: int) -> List[Subscription]:
    """
    Returns a list of subscriptions to that user id or None
    """
    return Subscription.query.filter_by(subscriber=userid).all()


def get_specific_subscription(subscriber_id: int, subscribed_id:int) -> Subscription:
    """
    Return the subscription between the two users, or None
    """
    return Subscription.query.filter_by(subscriber_id=subscriber_id, subscribed_id=subscribed_id).first()

def add_subscription(subscriber_id: int, subscribed_id:int):
    """
    Adds a subscription to the table, provided it is valid
    @raises ValueError if subscriber_id != subscribed_id or if one of the users doesn't exist
    """
    #no subscription to self
    if subscribed_id == subscriber_id:
        raise ValueError(f"Tried to subscribe user ID: {subscriber_id} to itself")
    #no double subscription
    if get_specific_subscription(subscriber_id,subscribed_id) is not None:
        raise ValueError(f"Subscription from {subscriber_id} to {subscribed_id} already exists")
    subscriber = find_user_by_id(subscriber_id)
    subscribed = find_user_by_id(subscribed_id)
    #check that users exist first
    if subscriber is None:
        raise ValueError(f"Subscriber did not exist, ID: {subscriber_id}")
    if subscribed is None:
        raise ValueError(f"Subscribed user did not exist, ID: {subscribed_id}")
    new_sub = Subscription(subscriber_id, subscribed_id)
    db.session.add(new_sub)
    db.session.commit()

def remove_subscription(subscription_id: int) -> None:
    """Removes a subscription with some id from the database
    """
    sub = Subscription.query.get(subscription_id)
    if sub is None:
        print("WARNING: Tried to remove a non-existant subscription")
        return
    
    db.session.delete(sub)
    db.session.commit()