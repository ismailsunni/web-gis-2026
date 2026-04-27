MARP = npx @marp-team/marp-cli --no-stdin
SRC  = ogc-services.md
HTML = ogc-services.html
PDF  = ogc-services.pdf

.PHONY: all html pdf serve clean

all: html pdf

html: $(HTML)
pdf:  $(PDF)

serve:
	PORT=8081 $(MARP) --server .

$(HTML): $(SRC)
	$(MARP) $(SRC) --html --output $(HTML)

$(PDF): $(SRC)
	$(MARP) $(SRC) --pdf --allow-local-files --output $(PDF)

clean:
	rm -f $(HTML) $(PDF)
