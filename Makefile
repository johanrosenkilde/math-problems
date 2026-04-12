D ?= 2.5
P ?= 10

all: math_problems.pdf

math_problems.pdf:
	uv run math-problems -p $(P) -d $(D) -o $@

addition.pdf:
	uv run math-problems -p $(P) -d $(D) -m addition -o $@

subtraction.pdf:
	uv run math-problems -p $(P) -d $(D) -m subtraction -o $@

multiplication.pdf:
	uv run math-problems -p $(P) -d $(D) -m multiplication -o $@

division.pdf:
	uv run math-problems -p $(P) -d $(D) -m division -o $@

counting-squares.pdf:
	uv run math-problems -p $(P) -d $(D) -m counting-squares -o $@

grocery-list.pdf:
	uv run math-problems -p $(P) -d $(D) -m grocery-list -o $@

clean:
	rm -f math_problems.pdf addition.pdf subtraction.pdf multiplication.pdf division.pdf counting-squares.pdf grocery-list.pdf

.PHONY: all clean math_problems.pdf addition.pdf subtraction.pdf multiplication.pdf division.pdf counting-squares.pdf grocery-list.pdf
