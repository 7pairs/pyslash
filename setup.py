from setuptools import find_packages, setup


setup(
    name='pyslash',
    version='1.0.0',
    description='Tools for parsing nikkansports.com',
    author='Jun-ya HASEBA',
    author_email='7pairs@gmail.com',
    url='http://seven-pairs.hatenablog.jp/',
    packages=find_packages(),
    entry_points="""\
    [console_scripts]
    pyslash = pyslash.pyslash:main
    """
)
