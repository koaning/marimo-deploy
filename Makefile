test:
	marimo export script app.py -o test.py
	pytest -v test.py
	rm test.py

clean:
	rm -rf test.py
 
install: 
	python -m pip install uv
	uv venv --seed
	uv pip install -r requirements.txt motest pytest httpx
	curl -L https://fly.io/install.sh | sh
