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
    include_package_data=True
)
