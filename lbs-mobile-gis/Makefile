MARP = npx @marp-team/marp-cli --no-stdin
SRC  = lbs-mobile-gis.md
HTML = lbs-mobile-gis.html
PDF  = lbs-mobile-gis.pdf

.PHONY: all html pdf serve diagrams clean

all: html pdf

html: $(HTML)
pdf:  $(PDF)

serve:
	PORT=8082 $(MARP) --server .

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
