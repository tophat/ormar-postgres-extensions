import sys
from datetime import datetime

from setuptools import (
    find_packages,
    setup,
)

python_requires = ">=3.6"
setup_requires = ["setuptools_scm"]
install_requires = [
    "databases[postgresql]>=0.5.4,<1.0.0",
    "ormar>=0.10.24,<1.0.0",
    "pydantic>=1.9.0,<2.0.0",
    "sqlalchemy>=1.4.29,<2.0.0",
]
test_requires = [
    "codecov",
    "coverage[toml]",
    "invoke",
    "psycopg2-binary",
    "pytest",
    "pytest-asyncio",
]
dev_requires = [
    "black",
    "flake8",
    "isort",
    "pip-tools",
    "py-githooks",
    "pygithub",
    "semver",
    "twine",
    "wheel",
    *test_requires,
]

if sys.version_info < (3, 6):
    raise RuntimeError("Only Python 3.6+ supported.")


def readme() -> str:
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def version_scheme(v):
    if v.exact:
        return v.format_with("{tag}")
    return datetime.now().strftime("%Y.%m.%d.%H%M%S%f")


if __name__ in ["__main__", "builtins"]:
    setup(
        name="ormar-postgres-extensions",
        description="PostgreSQL specific extensions to the Ormar ORM",
        author="Top Hat Open Source",
        author_email="opensource@tophat.com",
        license="Apache License 2.0",
        url="https://github.com/tophat/ormar-postgres-extensions",
        long_description=readme(),
        long_description_content_type="text/markdown",
        use_scm_version={
            "local_scheme": lambda _: "",
            "version_scheme": version_scheme,
            "write_to": "version.txt",
        },
        package_dir={"": "src"},
        package_data={"": ["VERSION"]},
        packages=find_packages("./src"),
        zip_safe=False,
        extras_require={"dev": dev_requires, "test": test_requires},
        install_requires=install_requires,
        setup_requires=setup_requires,
        python_requires=python_requires,
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Software Development :: Libraries",
        ],
    )
