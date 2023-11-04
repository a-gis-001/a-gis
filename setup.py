import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='a_gis',
    author='AEGIS 001',
    author_email='a-gis-001@proton.me',
    description='AEGIS',
    keywords='art, AI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/a-gis-001/a_gis',
    project_urls={
        'Documentation': 'https://github.com/a-gis-001/a_gis',
        'Bug Reports':
        'https://github.com/a-gis-001/a_gis/issues',
        'Source Code': 'https://github.com/a-gis-001/a_gis',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 1 - Planning',
        
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Image Processing',

        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=['pillow','numpy','pytest'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=a_gis:main',
    # You can execute `run` in bash to run `main()` in src/a_gis/__init__.py
    #     ],
    # },
)
