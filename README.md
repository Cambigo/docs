> [!CAUTION]
> I'm actively working on the notebook, particularly marp support. 
> **I recommend avoiding marp setup for now.**

# Notebook

This is my approach to building a local notebook (or one for github-pages), that can be used in day-to-day work.

## Setup

```shell
python -m venv ./.venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## mkdocs

To execute the mkdocs notebook for development of content:

```shell
mkdocs serve
```
The build the site for rendering through a web server, or to use with the FastAPI runner:

```shell
mkdocs build
```

## FastAPI

A minimal FastAPI script (`main.py`) is provided to serve the site directory after the site is built.

```shell
source .venv/bin/activate
mkdocs build
fastapi dev main.py
```

---

## For marp support

> [!WARNING]
> **NOT READY TO USE YET!**

If you use this, create a feature branch to test.  This will edit your content, and could break things.  I am working on improving, but it will be a while before I get back to it.

```shell
source .venv/bin/activate
npm install -g @marp-team/marp-cli
python scripts/marp.py
```

Encoding images for CSS:

- If you want to add new theme images, put them in the `marp/images/` directory.
- Remove the images from the end of `marp/notebook.css`.
- You must replace the `content.png` and `topic.png` files with your own.
- You can execute `python/encode.py >> marp/notebook.css` to append the encoded images to the css.

