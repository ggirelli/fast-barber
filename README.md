# fastx-barber

A Python3.6+ package to trim and extract flags from FASTA  and FASTQ files.

## Features

* Select your reads based on a pattern (regular expression).
* Trim your reads based on a pattern (regular expression).
* Extract parts (flags) of reads based on a pattern and store them in the read headers.
    - You can also extract the corresponding portions of the quality string too (only for fastq files).
* All patterns use the `regex` Python package to support [*fuzzy* matching](https://pypi.org/project/regex/#approximate-fuzzy-matching-hg-issue-12-hg-issue-41-hg-issue-109).
    - Using fuzzy matching might affect the barber's speed).
* You can also export reads that do not match the provided pattern.

## Requirements

`fastx-barber` has been tested with Python 3.6, 3.7, and 3.8. We recommend installing it using `pipx` (see [below](#install)) to avoid dependency conflicts with other packages. The packages it depends on are listed in our [dependency graph](https://github.com/ggirelli/fastx-barber/network/dependencies). We use [`poetry`](https://github.com/python-poetry/poetry) to handle our dependencies.

## Install

We recommend installing `fastx-barber` using [`pipx`](https://github.com/pipxproject/pipx). Check how to install `pipx` [here](https://github.com/pipxproject/pipx#install-pipx) if you don't have it yet!

Once you have `pipx` ready on your system, install the latest stable release of `fastx-barber` by running:
```
git clone https://github.com/ggirelli/fastx-barber
cd fastx-barber
pipx install .
```
If you see the stars (✨ 🌟 ✨), then the installation went well!

## Usage

Run:

* `fbarber` to access the barber's services.
* `fbarber trim` to trim your reads.
* `fbarber match` to select reads based on a pattern (regular expression).
* `fbarber extract` to extract parts of a read and store them in the read name, and then trim it.

Add `-h` to see the full help page of a command!

## Contributing

We welcome any contributions to `fastx-barber`. In short, we use [`black`](https://github.com/psf/black) to standardize code format. Any code change also needs to pass `mypy` checks. For more details, please refer to our [contribution guidelines](CONTRIBUTING.md) if this is your first time contributing! Also, check out our [code of conduct](CODE_OF_CONDUCT.md).

## License

`MIT License - Copyright (c) 2020 Gabriele Girelli`
