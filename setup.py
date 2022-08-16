from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hr_report/__init__.py
from hr_report import __version__ as version

setup(
	name="hr_report",
	version=version,
	description="hr custom report for erpnext",
	author="Ibrahim Morghim",
	author_email="morghim@outlook.sa",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
