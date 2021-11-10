# Relay Python Library

A Python client for the relay service which relays server-side messages to client-side subscribers (e.g. browser) via websockets.


## Installation

```
pip install relay-python
```

## Requirements

- Python 3.7+


# Usage

```Python

import relay

client = relay.Client('your_api_key...')

# Publish a message to subscribers over the nav channel
client.publish(
    ['global'],
    {
        'action': 'nav_update',
        'payload': {
            'inbox_unread': 2
        }
    }
)

# Close a subscriber with the user Id burt
client.close('burt')

```
