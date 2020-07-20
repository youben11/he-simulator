import setuptools


setuptools.setup(
    name="he-sim",
    version="0.1.0",
    author="Ayoub Benaissa",
    author_email="ayouben9@gmail.com",
    description="Simulate HE schemes for experimenting algorithms",
    keywords="homomorphic encryption simulation",
    packages=setuptools.find_packages(include=["he_sim", "he_sim.*"]),
    url="https://github.com/youben11/he-simulator",
    tests_require=["pytest"],
)
