default: 
	./quartermaster.py 12396
clean:
	rm -rf data/crew
	rm rummy.pyc | true
	cp -r backup/data ./
	cp backup/rummy.pyc ./
