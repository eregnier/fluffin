from setuptools import setup, find_packages

setup(
    name="fluffin",
    version="1.0.0",
    description="A simple static site generator tool",
    author="Eric Régnier",
    author_email="utopman@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="static site generator",
    install_requires=["jinja2", "httpwatcher"],
    entry_points={
        'console_scripts': [
            'fluffin=fluffin:run'
        ]
    }
)
