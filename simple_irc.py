"""
simple_irc: a simple, Pythonic IRC interface.

This module contains 2 classes: an IRC adapter, and a message wrapper.

Basic usage:
  >>> irc = simple_irc.IRC('mynick', '#python', 'irc.myserver.net')
  >>> for msg in irc: print(msg.sender + ': ' + msg)
  somebody: Hello, simple_irc!
  somebody_else: Oh hai there!
  >>> irc.write('Hi guys!')
"""

__author__ = "Max Rothman"
__copyright__ = "Copyright 2014 Max Rothman"
__license__ = "MIT"
__version__ = "1.0"

import socket, threading, time, sys
if sys.version_info.major < 3:
  import Queue
else: import queue as Queue

_wait = .01

class IRC(object):
  '''A simple IRC interface that can handle simultaneous reading and writing.
  Its interface is similar to those in the io module.'''

  def __init__(self, nick, channel, network, port=6667, future=False,
               mode=2, realname='Python simpleirc bot'):
    '''Initialize an IRC connection. By default, does not return until
    the connection is established.

      nick: the nickname to connect with
      channel: the name of the channel to connect to (e.g. "#python")
      network: the network to connect to (e.g. "irc.freenode.net")
      port: the port to connect on
      future: if True, will not connect until open() is called
      mode: bitmask of initial user mode. Only 'w' (2) and 'i' (4) are available.
      realname: real name field. Can be any string.
    '''

    self.nick = nick
    self.channel = channel
    self.network = network
    self.port = port
    self.mode = mode
    self.realname = realname

    self._readqueue = Queue.Queue()
    self._writequeue = Queue.Queue()
    self._closed = True

    if not future:
      self.open()


  def open(self):
    '''Open the connection. Does not return until the connection has been established.'''
    if not self._closed:
      raise IOError(self + " is already open")

    self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._soc.connect((self.network, self.port))
    self._soc.send('NICK {}\r\n'.format(self.nick).encode('UTF-8'))
    self._soc.send('USER {} {} * :{}\r\n'.format(self.nick, self.mode, self.realname).encode('UTF-8'))
    self._soc.send('JOIN {}\r\n'.format(self.channel).encode('UTF-8'))

    while True:
      #Read through all of the opening garbage
      data = self._soc.recv(4096).decode('UTF-8')
      
      #Error messages don't follow the same format as others, 
      #so we parse the code out early
      code = data.split()[1]
      if code.isdigit() and 400<=int(code)<=499:  
        raise ValueError(data.split(':')[2])
      elif "End of /NAMES list." in data:   #This is the last message before it's all good for some reason
        break
    
    self._soc.settimeout(_wait)   #the threads use this for nonblocking io
    self._closed = False

    tread = threading.Thread(target=self._reader)
    tread.daemon = True
    tread.start()

    twrite = threading.Thread(target=self._writer)
    twrite.daemon = True
    twrite.start()


  def _reader(self):
    '''Message reader thread'''
    while not self._closed:
      try: data = self._soc.recv(4096).decode('UTF-8')
      except socket.timeout: continue
      
      if 'PING' in data:  #so we don't get booted
        self._soc.send ('PONG ' + data.split()[1] + '\r\n')
      else:
        self._readqueue.put(message(data))

  def _writer(self):
    '''Message writer thread'''
    while not self._closed:
      time.sleep(_wait)
      if not self._writequeue.empty():
        msg = self._writequeue.get()
        self._writequeue.task_done()
        self._soc.send("PRIVMSG {} :{}\r\n".format(self.channel, msg).encode('UTF-8'))


  def __next__(self):
    msg = self.read()
    if msg is None:
      raise StopIteration
    else:
      return msg

  #Python2 compatability
  next = __next__

  def __iter__(self):
    return iter(self.read, None)

  def read(self):
    '''Returns the oldest unread message, or None if there are no unread messages.'''
    if self._readqueue.empty():
      return None
    else:
      msg = self._readqueue.get()
      self._readqueue.task_done()
      return msg

  def readall(self, limit=None):
    '''Returns a list of at most <limit> unread messages.
    If limit is unspecified, returns all unread messages.'''
    i = 0
    l = []
    for m in self:  #self is an iterable!
      l.append(m)
      i += 1
      if limit is not None and i>=limit:
        break

    return l

  def write(self, msg):
    '''Write a single message to the connected channel'''
    self._writequeue.put(msg)

  def writeall(self, msgs):
    '''Write all messages in an iterable to the connected channel'''
    for m in msgs:
      self.write(m)


  def close(self):
    '''Close the IRC connection'''
    self._closed = True
    time.sleep(2*_wait)   #wait for threads to terminate
    self._soc.send("QUIT\r\n".encode('UTF-8'))
    self._soc.close()
    del self._writequeue, self._readqueue

  @property
  def closed(self):
    '''True if the IRC connection is closed'''
    return self._closed


  def __enter__(self):
    return self

  def __exit__(self, exception_type, exception_value, traceback):
    self.close()
    return True



class message(str):
  '''An IRC message.

  Properties:
  - sender: the sender
  - hostname: the hostname of the sender
  '''
  def __new__(cls, raw):
    self = str.__new__(cls, raw.split(':')[2].rstrip())
    raw = raw.split(':')
    self.sender = raw[1].split('!')[0]
    self.hostname = raw[1].split()[0].split('@')[1]
    return self