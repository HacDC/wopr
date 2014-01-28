SHELL=/bin/bash

.PHONY: run push

run: $(BOTCONF) $(BOTDIR)/conf/users.conf
	supybot $(BOTCONFFILE)

push: clean
	git commit -a -m"automatic commit from Makefile"
	git push $(BOTREMOTE) $(BOTBRANCH)
