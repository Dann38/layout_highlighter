import setuptools

PACKAGE_DIR = {"": "."}
PACKAGES = setuptools.find_packages()
setuptools.setup(
    name="graph",
    version="0.0.1",
    author="Dunn Kopylov",
    author_email="38dunn@gmail.com",
    description="graph",

    package_dir=PACKAGE_DIR,
    packages=PACKAGES,

    python_requires=">=3.8"
)