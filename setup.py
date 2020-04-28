#!/usr/bin/env python
# coding: utf-8


from __future__ import print_function
from glob import glob
import json
from os.path import join as pjoin


from setupbase import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    find_packages,
    combine_commands,
    ensure_python,
    HERE,
)

from setuptools import setup


# The name of the project
name = "upsetjs_jupyter_widget"

with open("README.md") as readme_file:
    readme = readme_file.read()

# Ensure a valid python version
ensure_python(">=3.6")

with open("package.json") as pkg_file:
    pkg = json.load(pkg_file)

nb_path = pjoin(HERE, name, "nbextension", "static")
lab_path = pjoin(HERE, name, "labextension")

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, "index.js"),
    pjoin(HERE, "lib", "plugin.js"),
]

package_data_spec = {name: ["nbextension/static/*.*js*", "labextension/*.tgz"]}

data_files_spec = [
    ("share/jupyter/nbextensions/@upsetjs/jupyter_widget", nb_path, "*.js*"),
    ("share/jupyter/lab/extensions", lab_path, "*.tgz"),
    ("etc/jupyter/nbconfig/notebook.d", HERE, "upsetjs_jupyter_widget.json"),
]

cmdclass = create_cmdclass(
    "jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec
)
cmdclass["jsdeps"] = combine_commands(
    install_npm(HERE, build_cmd="build:all"), ensure_targets(jstargets),
)


if __name__ == "__main__":
    setup(
        name=name,
        description=pkg["description"],
        long_description=readme,
        long_description_content_type="text/markdown",
        version=pkg["version"],
        scripts=glob(pjoin("scripts", "*")),
        cmdclass=cmdclass,
        packages=find_packages(),
        author=pkg["author"]["name"],
        author_email=pkg["author"]["email"],
        url=pkg["homepage"],
        platforms="Linux, Mac OS X, Windows",
        keywords=["Jupyter", "Widgets", "IPython"],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Intended Audience :: System Administrators",
            "License :: Free For Home Use",
            "License :: Free for non-commercial use",
            "License :: Free For Educational Use",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Framework :: IPython",
            "Framework :: Jupyter",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Scientific/Engineering :: Visualization",
            "Typing :: Typed",
        ],
        include_package_data=True,
        install_requires=["ipywidgets>=7.5.0",],
        extras_require={
            "test": ["pytest>=3.6", "pytest-cov", "nbval",],
            "examples": [
                # Any requirements for the examples to run
            ],
            "docs": [
                "sphinx>=1.5",
                "recommonmark",
                "sphinx_rtd_theme",
                "nbsphinx>=0.2.13,<0.4.0",
                "jupyter_sphinx",
                "nbsphinx-link",
                "pytest_check_links",
                "pypandoc",
            ],
        },
        entry_points={},
    )
