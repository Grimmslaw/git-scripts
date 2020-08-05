from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='git-scripts',
    version='2.0.0',
    author='Wes Rickey',
    author_email='d.wrickey@gmail.com',
    description='Provides scripts useful for extending the functionality of git commands',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Grimmslaw/git-scripts.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
