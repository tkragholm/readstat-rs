from setuptools import setup, find_packages

setup(
    name="readstat-rs-dist",
    version="0.13.0",
    packages=find_packages(),
    package_data={
        'readstat_dist': ['bin/*'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'readstat=readstat-rs_dist.entry_point:main',
        ],
    },
)
