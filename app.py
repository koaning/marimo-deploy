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

__generated_with = "0.10.6"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        """
        ## Notebook to prod

        This notebook serves as a demonstration on how to deploy Marimo as a webapp that also carries an API. We will use spaCy as a motivating example. 

        You should see a simple spaCy demo below.
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

    @app.post("/api")
    def analyze_text(input_data: TextInput):
        return nlp(input_data.text).to_json()

    @app.post("/api")
    def analyze_text(input_data: TextInput, response_model=HTMLResponse):
        return render_text(input_data)
    return TextInput, analyze_text, app, nlp, read_root, render_text


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
def _(TextInput, mo, render_text, text_form):
    mo.Html(render_text(TextInput(text=text_form.value["text_in"]))) if text_form.value else None
    return


@app.cell
def _(nlp, text_form):
    import json

    json.dumps(nlp(text_form.value["text_in"]).to_json(), indent=2) if text_form.value else None
    return (json,)


@app.cell
def _(app, mo):
    if mo.app_meta().mode != "edit":
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
