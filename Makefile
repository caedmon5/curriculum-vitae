# File: Makefile

TEXFILE=CV
OUTPUT=CV.pdf

.PHONY: all clean cv

all: $(OUTPUT)

$(OUTPUT): $(TEXFILE).tex
	pdflatex $(TEXFILE).tex
	pdflatex $(TEXFILE).tex  # run twice for references

cv: all
	git add -A
	@read -p "Enter commit message (start with vN.n.n: to tag and publish a release): " msg; \
	if [ -z "$$msg" ]; then echo "Aborted: empty commit message"; exit 1; fi; \
	git commit -m "$$msg"; \
	git push; \
	ver=$$(printf '%s' "$$msg" | grep -oE '^v[0-9]+\.[0-9]+\.[0-9]+'); \
	if [ -n "$$ver" ]; then \
		echo "Tagging and publishing release $$ver ..."; \
		git tag -a "$$ver" -m "$$msg"; \
		git push origin "$$ver"; \
		notes=$$(printf '%s' "$$msg" | sed -E 's/^v[0-9]+\.[0-9]+\.[0-9]+:?[[:space:]]*//'); \
		gh release create "$$ver" "$(OUTPUT)" --title "$$ver" --latest --notes "$$notes"; \
	else \
		echo "No vN.n.n prefix in commit message — pushed without tag or release."; \
	fi

clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg $(OUTPUT)
