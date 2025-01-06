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

## Caveats

While this approach does work, there are a few notable downsides. 

- Because everything is in a single Python file we also need to have all the dependencies loaded during deployment. This suddenly also includes pytest and everything that we use for testing. 
- While we can easily deploy an API this way, it becomes a bit more involved to deploy the Marimo app together with the API in one go. You could construct the container to carry two running apps but it may be more pragmatic to consider two deployments instead. Or maybe deploy something on the side in the lines of [this blogpost](https://marimo.io/blog/github-notebooks-on-the-fly). 
