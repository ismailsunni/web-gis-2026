MARP = npx @marp-team/marp-cli --no-stdin
SRC  = lbs-mobile-gis.md
HTML = lbs-mobile-gis.html
PDF  = lbs-mobile-gis.pdf

.PHONY: all html pdf serve clean

all: html pdf

html: $(HTML)
pdf:  $(PDF)

serve:
	PORT=8082 $(MARP) --server .

$(HTML): $(SRC)
	$(MARP) $(SRC) --html --output $(HTML)

$(PDF): $(SRC)
	$(MARP) $(SRC) --pdf --allow-local-files --output $(PDF)

clean:
	rm -f $(HTML) $(PDF)
