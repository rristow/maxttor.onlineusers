from setuptools import setup, find_packages
import os

version = '1.1rc6'

setup(name='maxttor.sessioncontrol',
      version=version,
      description="Plone Product - Control the number of sessions for each user",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Plone sessions control online',
      author='Rodrigo Ristow',
      author_email='rodrigo@maxttor.com',
      url='https://github.com/rristow/maxttor.sessioncontrol',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['maxttor'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'pas.plugins.preauth==1.0',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
