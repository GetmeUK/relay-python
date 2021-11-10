
__all__ = [
    'Message',
    'Subscriber'
]


class Message:
    """
    A simple interface class for messaging.
    """

    @classmethod
    def send(cls, client, channels, message):
        """Send a message"""

        if isinstance(message, (list, dict)):
            message = client.encode(message)

        client(
            'post',
            f'pub',
            data={
                'channels': tuple(channels),
                'message': message
            }
        )


class Subscriber:
    """
    A simple interface class for subscribers.
    """

    @classmethod
    def close(cls, client, user_id):
        """Close a subscribers connection"""
        client('post', f'close', data={'user_id': user_id})
