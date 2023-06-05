INPUT_FILE=diploma
TA_FILE=technical_assignment
CLASS_FILE=preamble

all: pdf

pdf: ## Compile and clean
	xelatex -shell-escape -output-directory=out/ $(INPUT_FILE).tex
	xelatex -shell-escape -output-directory=out/ $(TA_FILE).tex

clean: ## Remove auxiliary files
	-rm out/$(INPUT_FILE).log out/$(INPUT_FILE).aux
	-rm out/$(CLASS_FILE).log out/$(CLASS_FILE).aux
	-rm out/$(TA_FILE).log out/$(TA_FILE).aux

full-clean: clean
	-rm out/$(INPUT_FILE).out out/$(INPUT_FILE).toc out/${INPUT_FILE}.pdf
	-rm out/$(TA_FILE).out out/$(TA_FILE).toc out/${TA_FILE}.pdf

lint:
	lacheck ${INPUT_FILE}
	lacheck ${TA_FILE}
