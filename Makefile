# File: Makefile

TEXFILE=CV
OUTPUT=CV.pdf

.PHONY: all clean cv short

all: $(OUTPUT)

VERSION ?= $(shell git describe --tags --always 2>/dev/null)

$(OUTPUT): $(TEXFILE).tex version.tex
	pdflatex -interaction=nonstopmode -halt-on-error $(TEXFILE).tex
	pdflatex -interaction=nonstopmode -halt-on-error $(TEXFILE).tex  # run twice for references

# Short version: same entries, without the \onlineonly summaries or the Appendix.
short: version.tex
	pdflatex -interaction=nonstopmode -halt-on-error -jobname=CV-short $(TEXFILE).tex
	pdflatex -interaction=nonstopmode -halt-on-error -jobname=CV-short $(TEXFILE).tex

.PHONY: version.tex
version.tex:
	printf '\\newcommand{\\cvversion}{%s}\n' '$(patsubst v%,%,$(VERSION))' > version.tex

# Read the message first, so a release builds with its own version number.
# (Building before tagging made each PDF show the previous release's number.)
cv:
	@read -p "Enter commit message (start with vN.n.n: to tag and publish a release): " msg; \
	if [ -z "$$msg" ]; then echo "Aborted: empty commit message"; exit 1; fi; \
	ver=$$(printf '%s' "$$msg" | grep -oE '^v[0-9]+\.[0-9]+\.[0-9]+'); \
	if [ -n "$$ver" ]; then $(MAKE) VERSION="$$ver" all || exit 1; \
	else $(MAKE) all || exit 1; fi; \
	git add -A; \
	git commit -m "$$msg"; \
	git push; \
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
