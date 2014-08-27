import hexfile

try:
    from setuptools import setup, Command
except:
    from distutils.core import setup, Command

'''
class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)
'''

setup(name='hexfile',
      version=hexfile.__version__,
      packages=['hexfile'],
      #cmdclass = {'test':PyTest},
      description='Library for loading and manipulating hex files.',
      author='Ryan Sturmer',
      author_email='ryansturmer@gmail.com',
      #install_requires=[],
      #tests_require=[],
      url='http://www.github.com/ryansturmer/hexfile')
