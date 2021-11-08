from setuptools import setup

setup(
    name="TextHTMLPress",
    version="0.1",
    description="A command-line static site generator.",
    license="MIT",
    author="Qiwen Yu",
    install_requires=["click", "setuptools"],
    entry_points={"console_scripts": ["TextHTMLPress = __main__:main"]},
)
