# marimo-deploy

Example of deploying a notebook that contains a FastApi app. 

## Base commands

You can toy with the notebook by installing everything and then running Marimo. 

```bash
python -m pip install -r requirements.txt
marimo edit app.py
```

You can also serve the FastApi app locally by running the same file as a script:

```bash
python app.py
```

You can even use `pytest` to test some pytests in the same file. 

```bash
# You can also run `make test`
marimo export script -o test.py app.py
pytest test.py
```

Finally, there is also a `Dockerfile` in the repo that you can easily deploy via `fly.io`. 

```bash
fly deploy
```