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
    include_package_data=True,
    install_requires=[
        'feedparser==5.2.1',
        'Flask==0.11.1',
        'Flask-Cache==0.13.1',
        'Flask-Mail==0.9.1',
        'Flask-OAuthlib==0.9.3',
        'Flask-Principal==0.4.0',
        'Flask-SQLAlchemy==2.1',
        'gevent==1.1.1',
        'gunicorn==19.3.0',
        'jieba==0.38',
        'Jinja2==2.8',
        'marshmallow==2.5.0',
        'mistune==0.7.1',
        'nose==1.3.7',
        'pypinyin==0.11.0',
        'python-dateutil==2.5.3',
        'simplejson==3.8.2',
        'Unidecode==0.4.19',
    ],
    dependency_links = ['https://github.com/fengluo/flask-themes/master#egg=flask_themes']
)
