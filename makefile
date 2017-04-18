default: 
	./quartermaster.py
clean:
	rm -rf data/crew
	rm rummy.pyc | true
	cp -r backup/data ./
	cp backup/rummy.pyc ./
