# Directories project

This project is a command-line script that supports an in-memory directory structure. It handles input for directory actions and does not interact with the host system.

**If not interested running the code, to see a recent execution, compare a [result log file](logs/) with the [expected-output.txt](test/expected-output.txt).**

## Setup

To get setup, use and install the python package and project manager [uv](https://docs.astral.sh/uv). Or use Python 3.12+ directly

### With uv

- if you don't have `uv`, install using brew or curl
  - `brew install uv`
  - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- run `uv` just to validate it installed
- run the setup
  - `uv venv` - this will setup a virtual environment for the project and automatically install or use the suggested python version.
  - `uv sync` - syncing ensures that all project dependencies are installed and up-to-date with the lockfile.
- execute the program, output will be in stdin and as a file in the recent log file in [logs/](logs)

```sh
uv run directories.py -f test/input.txt
```

### With python3

- If not using uv, ensure you have python 3.12+ or YMMV

```sh
python3 directories.py -f test/input.txt
```

## Running locally

Two ways to use the program:
1. File input
2. Using stdin

### File Input

Provide the suggested input file and the results will get printed to stdin and a log file in [logs](logs/). Input file will be a flag with `-f test/input.txt`.

### Stdin

Commands: `CREATE`, `LIST`, `MOVE`, or `DELETE`

Provide the following to stdin:
```
[COMMAND] [ARGS]...
```

Type in the commands one after another

Example input for CREATE:
```
CREATE apple/fruit
```

Example input for LIST:
```
LIST
```

Example input for MOVE
```
MOVE fruit/gala fruit/apple 
```

Example input for DELETE
```
DELETE fruit/apple
```

## Pytest

Repo has pytest setup to automatically run an execution given the [input.txt](test/input.txt) file and validate the most recent log file with the expected [output.txt](test/output.txt) file.

Running the test is just (if using uv this will just work):
```sh
pytest
```

## Expected Results
### INPUT
```text
CREATE fruits
CREATE vegetables
CREATE grains
CREATE fruits/apples
CREATE fruits/apples/fuji
LIST
CREATE grains/squash
MOVE grains/squash vegetables
CREATE foods
MOVE grains foods
MOVE fruits foods
MOVE vegetables foods
LIST
DELETE fruits/apples
DELETE foods/fruits/apples
LIST
```

### OUTPUT
```text
CREATE fruits
CREATE vegetables
CREATE grains
CREATE fruits/apples
CREATE fruits/apples/fuji
LIST
fruits
  apples
    fuji
grains
vegetables
CREATE grains/squash
MOVE grains/squash vegetables
CREATE foods
MOVE grains foods
MOVE fruits foods
MOVE vegetables foods
LIST
foods
  fruits
    apples
      fuji
  grains
  vegetables
    squash
DELETE fruits/apples
Cannot delete fruits/apples - fruits does not exist
DELETE foods/fruits/apples
LIST
foods
  fruits
  grains
  vegetables
    squash
```