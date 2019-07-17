from setuptools import setup, find_packages


setup(
    name='directory_sso_api_client',
    version='5.1.0',
    url='https://github.com/uktrade/directory-sso-api-client',
    license='MIT',
    author='Department for International Trade',
    description='Python API client for Export Directory.',
    packages=find_packages(exclude=["tests.*", "tests"]),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'directory_client_core>=6.0.0,<7.0.0',
    ],
    extras_require={
        'test': [
            'django>=2.2,<3.0a1',
            'requests>=2.18.4,<3.0.0',
            'pytest==3.6.0',
            'pytest-cov==2.3.1',
            'flake8==3.0.4',
            'requests_mock==1.1.0',
            'codecov==2.0.9',
            'twine>=1.11.0,<2.0.0',
            'wheel>=0.31.0,<1.0.0',
            'setuptools>=38.6.0,<39.0.0',
            'pytest-django>=3.2.1,<4.0.0',
            'pytest-sugar>=0.9.1,<1.0.0',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
