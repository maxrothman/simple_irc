from setuptools import setup
import simple_irc
setup(
  name = 'simple_irc',
  py_modules = ['simple_irc'],
  version = simple_irc.__version__,
  description = 'A simple, Pythonic IRC interface',
  author = 'Max Rothman',
  author_email = 'max.r.rothman@gmail.com',
  url = 'https://github.com/maxrothman/' + simple_irc.__name__,
  download_url = 'https://github.com/maxrothman/simple_irc/tarball/' + simple_irc.__version__,
  keywords = 'simple IRC',
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3'
  ],
)
