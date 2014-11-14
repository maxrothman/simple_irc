simple_irc
==========

A simple, Pythonic IRC interface

__Requirements:__ >Python2.6 (including Python3!)

Usage
---
1. Instantiate it

    ```
    myIRC = simple_irc.IRC("nickname", "channel", "irc.network.net")
    ```
    
2. Read from it

    ```
    >>> oldest_message = myIRC.read()
    "Hello, there!"
    ```
    
3. Write to it

    ```
    myIRC.write("Hello, world!")
    ```

4. Close it
    ```
    myIRC.close()
    ```
    
That's as simple as it gets!

Advanced Usage
---
Well, if you _insist_ on making it complicated, here you go.

This module contains 2 classes: `IRC`, and IRC interface, and `message`, a message wrapper.

####IRC
This class implements an interface similar to those in the [io module](https://docs.python.org/2/library/io.html). To read all unread messages, you can just iterate through it:

    for msg in myIRC:
        print(msg)

Additionally, it's a context manager:

    with simple_irc.iRC('nick', '#channel', 'irc.server.net') as myIRC:
        #do stuff

#####Methods
- `IRC(nick, channel, network, port=6667, future=False, mode=2, realname='Python simple_irc bot')`: Initialize an IRC connection. By default, does not return until the connection is established.
    - nick: the nickname to connect with
    - channel: the name of the channel to connect to (e.g. "#python")
    - network: the network to connect to (e.g. "irc.freenode.net")
    - port: the port to connect on
    - future: if True, will not connect until open() is called
    - mode: bitmask of initial user mode. Only 'w' (2) and 'i' (4) are available.
    - realname: real name field. Can be any string.
- `IRC.read()`: return the oldest message as a message object
- `IRC.readall(limit=None)`: return a list of at most <limit> unread messages. If limit is unspecified, return all unread messages.
- `IRC.write(msg)`: write a message (string) to the connected channel
- `IRC.writeall([msg1, msg2, ...])`: write all messages in an iterable to the connected channel
- `IRC.open()`: open the connection manually (if `future=True`)
- `IRC.close()`: close the connection gracefully
- `IRC.closed`: True if the connection is closed


####message
`message` is just a string with some extra properties to hold metadata:
- `message.sender`: the message sender
- `message.hostname`: the hostname of the sender