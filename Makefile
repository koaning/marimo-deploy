test:
	marimo export script app.py -o test.py
	pytest -v test.py
	rm test.py

clean:
	rm -rf test.py
 