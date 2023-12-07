from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent
VERSION_FILE = BASE_DIR / "dayone_to_obsidian" / "version.py"
README_FILE = BASE_DIR / "README.md"
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"


def read(path: Path) -> str:
    with path.open() as file:
        return file.read()


def get_version() -> str:
    """Get version from the package without actually importing it."""
    for line in read(VERSION_FILE).splitlines():
        if line.startswith("__version__"):
            return eval(line.split("=")[1])
    raise RuntimeError("section __version__ not found")


def readme() -> str:
    return read(README_FILE)


def requirements() -> list[str]:
    return read(REQUIREMENTS_FILE).splitlines()


setup(
    name="dayone-to-obsidian",
    version=get_version(),
    package_dir={"": "src"},
    description="DayOne to Obsidian Converter",
    author="Taras Drapalyuk",
    author_email="taras@drapalyuk.com",
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/kulapard/dayone-to-obsidian",
    download_url="https://github.com/kulapard/dayone-to-obsidian",
    long_description=readme(),
    install_requires=requirements(),
    python_requires=">=3.11",
    # TODO: add classifiers
    # classifiers=[],
    package_data={
        "dayone_to_obsidian": ["py.typed"],
    },
    entry_points={
        "console_scripts": ["dayone-to-obsidian = dayone_to_obsidian.cli:main"],
    },
    include_package_data=True,
)
