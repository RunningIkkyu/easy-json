import io

import setuptools 
from setuptools import find_packages

setuptools.setup(
    name='easyjson2',
    version='0.1.1',
    description='Get JSON quickly and easily',
    author='RunningIkkyu',
    author_email='389498623@qq.com',
    url='https://github.com/RunningIkkyu/easy-json',
    license='MIT',
    #long_description=io.open('README.md', encoding='utf-8').read(),
    test_suite = 'tests',
    packages=find_packages(),
    classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
