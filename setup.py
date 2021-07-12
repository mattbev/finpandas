"""
PyPI build file
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

docs_extras=[
    'sphinx==3.4.1',
    'docutils'
]

setuptools.setup(
    name="finpandas",
    version="0.1.0",
    author="Matthew Beveridge",
    author_email="mattjbev@gmail.com",
    description="U.S. Public Financial Analysis Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://finpandas.readthedocs.io/en/latest/",
    keywords=["SEC", "EDGAR", "finance", "10-K", "10-Q", "analytics", "investing"],
    install_requires=[
        "pandas",
        "pymysql",
        "sqlalchemy==1.4.*",
        "dpath",
        "regex"
    ],
    extras_require={
        'docs': docs_extras
    },
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
