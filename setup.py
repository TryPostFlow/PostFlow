from setuptools import setup, find_packages
setup(
    name='get-planet',
    version='0.1.0',
    author='Shawn Xie',
    author_email='fengluo17@gmail.com',
    url="https://github.com/fengluo/planet",
    license="Apache Licence 2.0",
    long_description="""
    This is blog system
    """,
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    include_package_data=True,
    entry_points='''
        [console_scripts]
        planet=planet.commands:planet
    ''',
    install_requires=[
        'feedparser==5.2.1',
        'Flask==0.12',
        'Flask-Mail==0.9.1',
        'Flask-OAuthlib==0.9.3',
        'Flask-Principal==0.4.0',
        'Flask-SQLAlchemy==2.1',
        'Flask-Themes2==0.1.4',
        'gevent==1.1.1',
        'gunicorn==19.6.0',
        'jieba==0.38',
        'Jinja2==2.9.5',
        'marshmallow==2.12.2',
        'mistune==0.7.1',
        'nose==1.3.7',
        'pypinyin==0.16.1',
        'python-dateutil==2.6.0',
        'simplejson==3.10.0',
        'Unidecode==0.4.20',
        'raven==6.0.0'
    ]
)
