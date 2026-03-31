MARP = npx @marp-team/marp-cli --no-stdin
SRC  = web-gis-development.md
HTML = web-gis-development.html
PDF  = web-gis-development.pdf

.PHONY: all html pdf diagrams clean

all: html pdf

html: $(HTML)
pdf:  $(PDF)

$(HTML): $(SRC)
	$(MARP) $(SRC) --html --output $(HTML)

$(PDF): $(SRC)
	$(MARP) $(SRC) --pdf --allow-local-files --output $(PDF)

diagrams:
	cd diagrams && for f in *.mmd; do \
		npx @mermaid-js/mermaid-cli -i "$$f" -o "$${f%.mmd}.png" -t default -b white -w 1200; \
	done

clean:
	rm -f $(HTML) $(PDF)
