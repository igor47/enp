# ENP: Evergrow Number Printer

This repo contains a sample interview problem for Evergrow.
It's a web app which accepts numbers from a user, and prints them as a PDF.

There are a few interesting features about this app:
* all local functionality is implemented as a typer app, including launching in dev/prod + builds + tests/linting
* the backend is python and the front-end is a [Vue 3](https://vuejs.org/guide/introduction.html) SPA built via [Vite](https://vitejs.dev/guide/#overview)

This was intended as a playground for me to learn Vue 3 and Vite.
There's some complexity around dev env, where the Vite server provides hot module reloading, but has to proxy API requests back to the flask server.

## Setup

The author uses `asdf` and `direnv` to manage this codebase.
This requires a `.envrc` file in the directory root, like so:

```
use asdf;
layout python3;
```

This allows a virtualenv to be immediately activated upon changing into this directory.

### Dependencies

Dependencies are managed with poetry.
You will need `poetry` installed into your virtualenv or global python environment:

```
$ pip install poetry
```

After that, install the project w/ all dependencies:

```
$ poetry install
```

## Running

The entry-point for the project is the binary `enp`, available after you've run `poetry install`.
To get help:

```
$ enp --help
```

To run the dev server:

```
$ enp run dev
```

## Tests

The entry point for tests is the command `enp tests`.
To run all tests:

```
$ enp tests all
```
