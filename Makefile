# File: Makefile

TEXFILE=CV
OUTPUT=CV.pdf
DOCS_DIR=docs

.PHONY: all clean deploy

all: $(OUTPUT)

$(OUTPUT): $(TEXFILE).tex
	pdflatex $(TEXFILE).tex
	pdflatex $(TEXFILE).tex  # run twice for references

deploy: all
	mkdir -p $(DOCS_DIR)
	cp $(OUTPUT) $(DOCS_DIR)/$(OUTPUT)
	cp index.html $(DOCS_DIR)/index.html
	git add $(DOCS_DIR)/$(OUTPUT) $(DOCS_DIR)/index.html
	@read -p "Enter commit message: " msg; \
	if [ -z "$$msg" ]; then echo "Aborted: empty commit message"; exit 1; fi; \
	git commit -m "$$msg"; \
	git push

clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg $(OUTPUT)
