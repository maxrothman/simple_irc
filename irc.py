#!/usr/bin/python

import socket, threading, time, Queue

class irc(object):
  '''A simple IRC interface that can handle simultaneous reading and writing.

  Initiating an instance connects to the specified channel and doesn't return
  until the connection is complete.
  '''

  def __init__(self, nick, channel, network, port=6667):
    self.channel = channel
    self.nick = nick
    self.network = network
    self._readqueue = Queue.Queue()
    self._writequeue = Queue.Queue()

    self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    self.irc.connect ( ( network, port ) )
    self.irc.send ( 'NICK {}\r\n'.format(nick) )
    self.irc.send ( 'USER {0} {0} {0} :Python IRC\r\n'.format(nick) )
    self.irc.send ( 'JOIN {}\r\n'.format(channel) )

    self.ready = False
    self.stop = False
    tread = threading.Thread(target=self._reader)
    tread.daemon = True
    tread.start()

    twrite = threading.Thread(target=self._writer)
    twrite.daemon = True
    twrite.start()

    while not self.ready:
      pass


  def _reader(self):
    '''Message reader thread'''
    while not self.stop:
      time.sleep(.01) 
      data = self.irc.recv(4096)
      
      if "End of /NAMES list." in data:   #this is the last thing that prints, for some reason
        self.ready = True
      elif 'PING' in data:  #so we don't get booted
        self.irc.send ('PONG ' + data.split()[1] + '\r\n')
      elif self.ready:
        self._readqueue.put( data.split(":")[-1].strip() )


  def read(self):
    '''Returns the oldest unread message, or None if there are none left'''
    if self._readqueue.empty():
      return None
    else:
      data = self._readqueue.get()
      self._readqueue.task_done()
      return data


  def _writer(self):
    '''Message writer thread'''
    while not self.ready:
      pass
    while not self.stop:
      time.sleep(.01)
      if not self._writequeue.empty():
        msg = self._writequeue.get()
        self.irc.send("PRIVMSG {} :{}\r\n".format(self.channel, msg))
        self._writequeue.task_done()

    self.irc.send("QUIT\r\n")


  def write(self, msg):
    '''Writes <msg> to the connected channel'''
    self._writequeue.put(msg)


  def close(self):
    '''Close the IRC connection'''
    self.stop = True
    time.sleep(.1)
    self.irc.close()