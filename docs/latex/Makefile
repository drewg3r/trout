INPUT_FILE=diploma
CLASS_FILE=preamble

all: pdf-clean

pdf-clean: ## Compile and clean
	xelatex -shell-escape -output-directory=out/ $(INPUT_FILE).tex
	make clean

clean: ## Remove auxiliary files
	-rm out/$(INPUT_FILE).log out/$(INPUT_FILE).aux
	-rm out/$(CLASS_FILE).log out/$(CLASS_FILE).aux

full-clean: clean
	-rm out/$(INPUT_FILE).out out/$(INPUT_FILE).toc out/${INPUT_FILE}.pdf

lint:
	lacheck ${INPUT_FILE}
