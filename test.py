
from bson.objectid import ObjectId

from relay.client import Client
from relay.resources import Message, Subscriber


client = Client(
    (
        '5LpAS6ddRTOEGQUO8kZyBlze9SxjJLbmoLxptY5Sps1KcM42r2p95iYBdFtwXwin0KL4'
        'ryLjmLe_VkzEh1sBfVCyHP7VexpX9re42y1axWZmEH2Y1BjuO9ZRlQSAwl1cCGq00UHc'
        'Ic4Vg-xmS2TtV-Hi-tUMeNNXnaKbhXmckGs'
    ),
    'http://api.relay.local'
)

Message.send(
    client,
    ['global'],
    {
        'action': 'nav_update',
        'cursor': str(ObjectId()),
        'payload': {
            'inbox': 2
        }
    }
)

Subscriber.close(client, 'ant@getme.co.uk')

Message.send(
    client,
    ['global'],
    {
        'action': 'nav_update',
        'cursor': str(ObjectId()),
        'payload': {
            'inbox': 1
        }
    }
)

