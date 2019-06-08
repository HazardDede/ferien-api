from setuptools import setup, find_packages


VERSION = '0.3.4'


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='ferien-api',
    version=VERSION,
    description="Python client library for ferien-api.de",
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/HazardDede/ferien-api',
    author='Dennis Muth',
    author_email='den.muth@googlemail.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='ferien api client',
    project_urls={
        'Documentation': 'https://github.com/HazardDede/ferien-api/blob/master/README.mdpp',
        'Source': 'https://github.com/HazardDede/ferien-api/',
        'Tracker': 'https://github.com/HazardDede/ferien-api/issues',
    },
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'aiohttp>=3.5.0',
        'attrs>=18.0.0',
        'pytz>=2015.2',
        'requests>=2.0.0'
    ],
    python_requires='>=3.5',
    include_package_data=True
)
