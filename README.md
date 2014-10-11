simple_irc
==========

A simple, Pythonic IRC interface

Usage
---
1. Instantiate it
2. 
    ```
    myIRC = irc.irc(nickname, channel, irc.network.net)
    ```
    
2. Read from it

    ```
    oldest_message = myIRC.read()
    ```
    
3. Write to it

    ```
    myIRC.write("Hello, world!")
    ```
    
That's as simple as it gets.
