# Textual Editor

Get [uv](https://docs.astral.sh/uv/)

## Install directly from GitHub

```sh
uv tool install git+https://github.com/kyrlian/textual-editor.git
```

run with `ted <file name>`

## or clone locally

Clone:

```sh
git clone https://github.com/kyrlian/textual-editor.git
cd textual-editor
```

## Run

Run the project script directly with uv:

```sh
uv run .\textual_editor\app.py
```

Run the project script without installation with uvx:
```sh
uvx --from . ted
```
## Install

Install and run uv tools:

```sh
uv tool install .
```

run with `ted <file name>`

Uninstall:

```sh
uv tool uninstall textual-editor
```
