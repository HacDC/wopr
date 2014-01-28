SHELL: /bin/bash

.PHONY: run clean push

WOPRJr.conf:
	sed -i 's/%(ident_password)s/$(IDENT_PASSWORD)/g' WOPRJr.conf

conf/users.conf:
	if ! [ -e conf/users.conf ] ;then
		@echo ERROR please link users.conf to config/users.conf
	fi

run: WOPRJr.conf conf/users.conf
	supybot WOPRJr.conf

clean:
	sed -i 's/$(IDENT_PASSWORD)/%(ident_password)s/g' WOPRJr.conf
	rm conf/users.conf

push: clean
	git commit -a -m"automatic commit from Makefile"
	git push origin master



