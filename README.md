<p align="center"></p>
<h2 align="center">Check Bump</h2>
<p align="center">
<a href="https://github.com/rgryta/Check-Bump/actions/workflows/main.yml"><img alt="Build" src="https://github.com/rgryta/Check-Bump/actions/workflows/main.yml/badge.svg?branch=main"></a>
<a href="https://pypi.org/project/check-bump/"><img alt="PyPI" src="https://img.shields.io/pypi/v/check-bump"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/PyCQA/pylint"><img alt="pylint" src="https://img.shields.io/badge/linting-pylint-yellowgreen"></a>
<a href="https://github.com/rgryta/NoPrint"><img alt="NoPrint" src="https://img.shields.io/badge/NoPrint-enabled-blueviolet"></a>
</p>

## About

Want to add version bump checks to your CI/CD pipeline? This packages makes it easy.
Simply execute `check-vbump` within a directory where your `pyproject.toml` is located.

If there was a version bump, process will finish with exit code 0 - read stdout for the new version.
Otherwise, process will finish with exit code 1.

## Requirements

This package requires `tomlkit` package.
