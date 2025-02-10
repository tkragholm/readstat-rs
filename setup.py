from pathlib import Path

from setuptools import find_packages, setup

# Read version from __version__.py
about = {}
here = Path(__file__).parent
with open(here / "readstat_rs" / "__version__.py", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="readstat_rs_dist",
    version=about["__version__"],
    packages=find_packages(include=["readstat_rs", "readstat_rs.*"]),
    package_data={
        "readstat_rs": ["bin/*"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "readstat=readstat_rs.entry_point:main",
        ],
    },
    python_requires=">=3.7",
)
