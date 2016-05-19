target=Lettering-Regular.ttf

all: $(target)
source_font: special_elite/special_elite.zip oradano_mincho/oradano_mincho.zip

FF=fontforge
FFFLAGS=-lang=py

special_elite/special_elite.zip:
	mkdir -p special_elite
	cd special_elite && curl -o special_elite.zip https://www.fontsquirrel.com/fonts/download/special-elite
	cd special_elite && unzip special_elite.zip

oradano_mincho/oradano_mincho.zip:
	mkdir -p oradano_mincho
	cd oradano_mincho && curl -o oradano_mincho.zip http://www.asahi-net.or.jp/~sd5a-ucd/freefonts/Oradano-Mincho/Oradano2016-0427t.zip
	cd oradano_mincho && unzip oradano_mincho.zip

$(target): source_font
	$(FF) $(FFFLAGS) -script lettering.py

clean:
	rm -rf $(target)

all-clean: clean
	rm -rf special_elite oradano_mincho
