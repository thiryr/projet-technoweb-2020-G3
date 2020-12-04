from app import db
from app.models.subscription import Subscription

class SubscriptionRepository:

    @staticmethod
    def find_subscriptions_from(userid: int) -> [Subscription]:
        """
        Returns a list of subscription from that user id or None
        """
        return User.query.filter_by(subscriber=userid)

    def find_subscriptions_to(userid: int) -> [Subscription]:
        """
        Returns a list of subscriptions to that user id or None
        """
        return User.query.filter_by(subscriber=userid)