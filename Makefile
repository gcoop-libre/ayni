LIBDIR = $(DESTDIR)/usr/share/pyshared/ayni
BINDIR = $(DESTDIR)/usr/games
DESKDIR = $(DESTDIR)/usr/share/applications
ICONDIR = $(DESTDIR)/usr/share/pixmaps

clean:
	rm -f *.py[co] */*.py[co]

install:
	mkdir -p $(LIBDIR)
	mkdir -p $(BINDIR)
	mkdir -p $(DESKDIR)
	mkdir -p $(ICONDIR)
	cp -R data $(LIBDIR)
	cp *.py $(LIBDIR)
	cp ayni $(BINDIR)
	cp desktop/ayni.desktop $(DESKDIR)
	cp desktop/ayni48.png $(ICONDIR)
	cp desktop/ayni.xpm $(ICONDIR)


uninstall:
	rm -rf $(LIBDIR)
	rm $(BINDIR)/ayni
	rm $(DESKDIR)/ayni.desktop
	rm $(ICONDIR)/ayni48.png $(ICONDIR)/ayni.xpm
