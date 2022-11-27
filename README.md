# datasette-export

[![PyPI](https://img.shields.io/pypi/v/datasette-export.svg)](https://pypi.org/project/datasette-export/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-export?include_prereleases&label=changelog)](https://github.com/simonw/datasette-export/releases)
[![Tests](https://github.com/simonw/datasette-export/workflows/Test/badge.svg)](https://github.com/simonw/datasette-export/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-export/blob/main/LICENSE)

Export pages from Datasette to disk

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-export

## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-export
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
