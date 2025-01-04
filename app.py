# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastapi==0.115.6",
#     "marimo",
#     "pydantic==2.10.4",
#     "spacy==3.8.3",
#     "uvicorn==0.34.0",
# ]
# ///

import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        """
        # Notebook to prod

        This notebook serves as a demonstration on how to deploy Marimo as a webapp that also carries an API. We will use spaCy as a motivating example. 

        ## Base usecase

        You can use the textbox below to type any English text that you like. When you submit the text will be passed to a `en_core_web_sm` model to extract some entities together with some other linguisitc information. Note that this model is designed to be lightweight, not to be the most effective model out there.
        """
    )
    return


@app.cell
def _(BaseModel, FastAPI, HTMLResponse, render, spacy):
    # Load English language model
    nlp = spacy.load("en_core_web_sm")

    # Initialize FastAPI app
    app = FastAPI(
        title="NLP API",
        description="A simple API for text analysis using spaCy",
        version="1.0.0"
    )

    class TextInput(BaseModel):
        text: str

    def render_text(text_input: TextInput):
        doc = nlp(text_input.text)
        return render(doc, style="ent")

    @app.get("/health")
    @app.get("/healthz")
    def read_root():
        return {"status": "alive"}

    @app.post("/api/json")
    def analyze_text(input_data: TextInput):
        return nlp(input_data.text).to_json()

    @app.post("/api/viz")
    def analyze_text_viz(input_data: TextInput, response_model=HTMLResponse):
        return HTMLResponse(content=render_text(input_data))
    return (
        TextInput,
        analyze_text,
        analyze_text_viz,
        app,
        nlp,
        read_root,
        render_text,
    )


@app.cell
def _(mo):
    text_form = (
        mo.md("{text_in}")
          .batch(text_in=mo.ui.text_area(label="Input text", placeholder="Hi. My name is Vincent."))
          .form()
    )

    text_form
    return (text_form,)


@app.cell
def _(mo):
    mo.md("""You can see a nice render of the extracted entities below.""")
    return


@app.cell
def _(TextInput, mo, render_text, text_form):
    mo.Html(render_text(TextInput(text=text_form.value["text_in"]))) if text_form.value else None
    return


@app.cell
def _(mo):
    mo.md("""The api can return this visualisation at `/api/viz` but you can also get the following json at `/api/json`.""")
    return


@app.cell
def _(nlp, text_form):
    import json

    json.dumps(nlp(text_form.value["text_in"]).to_json(), indent=2) if text_form.value else None
    return (json,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Production stuff

        ### The webapp 

        The Marimo notebook contains the code to run this task, but it also has a FastApi app built in that re-uses all the helper functions. The notebook also has a cell that contains this line:

        ```python
        if mo.app_meta().mode == "script":
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8080)
        ```

        That means that when you run the notebook as a script that it can start a server for you! This makes everything nice and self contained! Locally you can experiment away in a notebook and when you are ready to re-use these parts you don't need to move things into a seperate Python module, you can just deploy the server in the notebook as you would normally.

        ### Tests

        You can run a Marimo notebook with `python` to run it as a script but you can also add tests for `pytest`. This will allow you also have all sorts of tests attached to really keep the notebook self-contained. This notebook comes with some of these unit-tests added that check for a few basics on the FastApi app. The CI flow for this particular notebook is to 

        ### Docker 

        Because Marimo is just a Python script it is also pretty easy to come up with a `Dockerfile` to deploy the whole thing. The only thing that is a bit "different" about this setup is that one might usually prefer `uv` these days, but `uv` cannot download spaCy models just due to an upstream issue. That's why this file sticks to `pip` for now. 

        ```Dockerfile
        FROM python:3.12
        WORKDIR /app
        COPY . .
        EXPOSE 8080
        RUN python -m venv venv && venv/bin/python -m pip install -r requirements.txt && venv/bin/python -m spacy download en_core_web_sm
        CMD ["venv/bin/python", "app.py"]
        ```

        ### Want to do more? 

        There are loads of things that you can do on top of this demo. Feel free to fork it from [Github](https://github.com/koaning/marimo-deploy) and make some changes. 

        - Right now the repository assumes a deployment on [fly.io](fly.io) but you can also use the setup to deploy elsewhere, like Huggingface.
        - You can choose to use a custom spaCy model that you trained yourself or many an LLM model like [GliNER](https://calmcode.io/shorts/gliner.py). Be aware that these kinds of models do require a fair bit more RAM so you may not be able to run this stack on free-tiered environments.
        - We may be able to extend this idea to scikit-learn models where we also train the model from inside the notebook. We need to take a few extra steps to make sure that we do not train if we do not need to. 
        """
    )
    return


app._unparsable_cell(
    r"""
    dtyoutdimport pytest
    from starlette.testclient import TestClient

    client = TestClient(app)

    @pytest.mark.parametrize(\"path\", (\"/health\", \"/healthz\"))
    def test_heatlh_endpoints(path):
        resp = client.get(path)
        assert resp.status_code == 200

    @pytest.mark.parametrize(\"path\", (\"/api/json\", \"/api/viz\"))
    def test_api_endpoints(path):
        json_blob = {\"text\": \"Hi. My name is Vincent\"}
        resp = client.post(path, json=json_blob)
        assert resp.status_code == 200
    """,
    name="_"
)


@app.cell
def _(app, mo):
    if mo.app_meta().mode == "script":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8080)
    return (uvicorn,)


@app.cell
def _():
    import marimo as mo
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel
    import spacy
    from spacy.displacy import render

    # Note that if you use `uv` to install packages that you will want to install the spaCy model by using this URL directly. 

    # ```
    # uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0.tar.gz
    # ```

    # The usual `spacy download` command has not been ported to understand `uv` just yet.
    return BaseModel, FastAPI, HTMLResponse, mo, render, spacy


if __name__ == "__main__":
    app.run()
