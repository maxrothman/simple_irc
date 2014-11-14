from distutils.core import setup
import simple_irc
setup(
  name = 'simple_irc',
  packages = ['simple_irc'],
  version = simple_irc.__version__,
  description = 'A simple, Pythonic IRC interface',
  author = 'Max Rothman',
  author_email = 'max.r.rothman@gmail.com',
  url = 'https://github.com/maxrothman/' + simple_irc.__name__,
  download_url = 'https://github.com/maxrothman/simple_irc/tarball/' + simple_irc.__version__,
  keywords = ['IRC', 'simple'],
  classifiers = [],
)