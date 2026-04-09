# math-problems

CLI tool that generates printable PDF math problem sheets for elementary school students (grades 1-6).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Usage

```
uv run math-problems [OPTIONS]
```

### Options

| Option | Default | Description |
|---|---|---|
| `-p`, `--pages` | 1 | Number of pages to generate |
| `-d`, `--difficulty` | 1 | Difficulty level (1-3) |
| `-m`, `--module` | all | Comma-separated problem types (see below) |
| `-l`, `--locale` | da | Language for titles: `en`, `da` |
| `-o`, `--output` | math_problems.pdf | Output PDF path |

### Modules

- `addition` - Addition problems
- `subtraction` - Subtraction problems
- `multiplication` - Multiplication problems (asymmetric difficulty ranges)
- `division` - Division problems (divisor >= 2, result always integer)
- `counting-squares` - Count filled squares in an N x N grid
- `grocery-list` - Multiply-and-add with grocery emoji placeholders

### Examples

Generate 10 pages of mixed problems at difficulty 2:

```
uv run math-problems -p 10 -d 2
```

Generate multiplication-only sheets in English:

```
uv run math-problems -p 5 -m multiplication -l en
```

## Running tests

```
uv run pytest
```