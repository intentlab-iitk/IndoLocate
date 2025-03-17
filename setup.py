from setuptools import setup, find_packages

# Helper function to read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()

setup(
    name="indolocate",
    version="0.1.0",
    author="Aravind Potluri",
    author_email="aravindswami135@gmail.com",
    description="A package for indoor localization using ML.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/intentlab-iitk/indolocate",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "indolocate-preprocess=indolocate.scripts.preprocess:main",
            "indolocate-train-knn=indolocate.scripts.train_knn:main",
            "indolocate-train-rf=indolocate.scripts.train_rf:main",
            "indolocate-test-knn=indolocate.scripts.test_knn:main",
            "indolocate-test-rf=indolocate.scripts.test_rf:main",
        ]
    },
    python_requires=">=3.7",
)
