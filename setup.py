import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='unred',
    version=__import__('unred').__version__,
    author='Przemysław Bruś',
    description='A library to determine the interstellar extinction.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pbrus/unredden-stars',
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=[
        'numpy==1.14.5',
        'scipy==1.1.0',
    ],
    tests_require=['pytest'],
    keywords=['reddening', 'extinction', 'stars'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Utilities'
    ],
)
