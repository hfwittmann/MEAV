from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
            return f.read()

setup(name='MEAV',
      version='0.0.1',
      description='Memory, Environment, Agent, Value',
      long_description=readme(),
      install_requires=['markdown'],
      packages=find_packages(),
      license='MIT',
      author='H. Felix Wittmann',
      author_email='hfwittmann@gmail.com',
      test_suite='nose.collector',
      tests_require='nose'
      )
