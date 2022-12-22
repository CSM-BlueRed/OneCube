from setuptools import setup, find_packages
import onecube


setup(
    name = onecube.__title__,
    version = onecube.__version__,
    author = onecube.__author__,
    description = onecube.__description__,
    packages = find_packages(),
    install_requires = ['requests', 'bs4'],
    keywords = ['minecraft', 'api', 'onecube'],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Natural Language :: French',
        'Programming Language :: Python',
        'Typing :: Typed'
    ]
)