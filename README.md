# Directories project

This project is a command-line script that supports an in-memory directory structure. It handles input for directory actions and does not interact with the host system.

## Setup

To get setup, use and install the python package and project manager [uv](https://docs.astral.sh/uv). Or use Python 3.12+ directly

### With uv

- if you don't have `uv`, install using brew or curl
  - `brew install uv`
  - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- run `uv` just to validate it is working
- run a sync in the root directory of this project: `uv sync`
  - This will install the specific version of python for the project as well as install any dependencies
- execute the program: `uv run directories.py -f test/input.txt`

### With python3

- Ensure you have python 3.12+
- `python3 directories.py -f test/input.txt`

## Usage

Two ways to use the program. 
1. File input
2. Using stdin

### File Input

Provide an input file and the results will get 

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
CREATE fruit/apple
CREATE fruit/gala

MOVE fruit/gala fruit/apple 
```

Example input for DELETE
```
CREATE fruit/apple

DELETE fruit/apple
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