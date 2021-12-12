import setuptools
import sys
version = "0.3.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires=[""]

setuptools.setup(
    name="GcodeController",
    version=version,
    description="Send gcode commands",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/guysoft/remote-office",
    author="Guy Sheffer",
    author_email="gusyoft@gmail.com",
    license="GPLv3",
    py_modules=["gcodecontroller"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={
        "": "src",
    },
    data_files=[],
    include_package_data=True,
    install_requires=install_requires,
    entry_points={"console_scripts": ["powerbeatsvr=powerbeatsvr.writer:run"]}
)