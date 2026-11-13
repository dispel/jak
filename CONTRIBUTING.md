# Contributing to jak

Bug reports, documentation fixes and code are all welcome. If you are unsure whether something is worth doing, open an [issue](https://github.com/dispel/jak/issues) and ask first.

## Reporting a bug

Open an [issue](https://github.com/dispel/jak/issues) and include:

- the output of `jak --version` and `python3 --version`
- your operating system
- the command you ran and the full output

Security problems are handled differently, see [docs/security.rst](docs/security.rst).

## Making a change

1. Set up your machine as described in the [contributor guide](docs/guide/contributor.rst).
2. Make your change on a branch or a fork.
3. Add or update tests for anything that changes behaviour, and run `pytest`.
4. If users will notice the change, add an entry to [docs/changelog.rst](docs/changelog.rst).
5. Open a pull request. GitHub Actions runs the tests on every supported Python version, and one of the stewards reviews it.

Small pull requests that do one thing are the easiest to review.

## License

jak is licensed under [Apache-2.0](LICENSE). As section 5 of that license says, contributions you submit are under the same terms.
