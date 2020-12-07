"""class for static methods around the Subscription table"""

from app import db
from app.models.subscription import Subscription
from app.repositories.users import UserRepository

class SubscriptionRepository:

    @staticmethod
    def find_subscriptions_from(userid: int) -> [Subscription]:
        """
        Returns a list of subscription from that user id or None
        """
        return Subscription.query.filter_by(subscriber=userid)

    @staticmethod
    def find_subscriptions_to(userid: int) -> [Subscription]:
        """
        Returns a list of subscriptions to that user id or None
        """
        return Subscription.query.filter_by(subscriber=userid)

    @staticmethod
    def add_subscription(subscriber_id: int, subscribed_id:int):
        """
        Adds a subscription to the table, provided it is valid
        @raises ValueError if subscriber_id != subscribed_id or if one of the users doesn't exist
        """

        if subscribed_id == subscriber_id:
            raise ValueError(f"Tried to subscribe user ID: {subscriber_id} to itself")

        subscriber = UserRepository.find_user_by_id(subscriber_id)
        subscribed = UserRepository.find_user_by_id(subscribed_id)

        #check that users exist first
        if subscriber == None:
            raise ValueError(f"Subscriber did not exist, ID: {subscriber_id}")
        if subscribed == None:
            raise ValueError(f"Subscribed user did not exist, ID: {subscribed_id}")


        new_sub = Subscription(subscriber_id, subscribed_id)

        db.session.add(new_sub)

        db.session.commit()
