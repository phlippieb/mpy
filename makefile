run: run.py
	python run.py

clean:
	find . -name *.pyc -exec rm {} +

test:
	pytest
