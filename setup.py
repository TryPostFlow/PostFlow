from setuptools import setup, find_packages
setup(
    name='postflow',
    version='0.1.1',
    author='Shawn Xie',
    author_email='fengluo17@gmail.com',
    url="https://github.com/TryPostFlow/PostFlow",
    license="Apache Licence 2.0",
    long_description="""
    A simple, powerful publishing platform
    """,
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    include_package_data=True,
    entry_points='''
        [console_scripts]
        postflow=postflow.commands:postflow
    ''',
    install_requires=[
        'feedparser==6.0.8', 'Flask==2.3.2', 'Flask-Storage==0.1.2',
        'Flask-Mail==0.9.1', 'Flask-OAuthlib==0.9.6', 'Flask-Principal==0.4.0',
        'Flask-Alembic==2.0.1', 'Flask-SQLAlchemy==2.5.1',
        'Flask-Themes2==1.0.0', 'SQLAlchemy-Utils==0.37.8', 'gevent==21.8.0',
        'gunicorn==20.1.0', 'jieba==0.38', 'Jinja2==3.0.1',
        'marshmallow==2.16.3', 'mistune==0.7.1', 'nose==1.3.7',
        'pypinyin==0.16.1', 'python-dateutil==2.6.0', 'simplejson==3.10.0',
        'Unidecode==0.4.20', 'feedwerk==1.0.0','raven==6.10.0'
    ])
