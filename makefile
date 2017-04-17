default: 
	./quartermaster
clean:
	rm -rf data/crew
	rm rummy.pyc | true
	cp backup/rummy.pyc ./
