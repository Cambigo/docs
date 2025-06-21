

# Welcome to the Notebook

For full documentation visit [chriscompton.github.io/notebook](https://chriscompton.github.io/notebook/).

## MkDocs Commands

* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.

## Marp Commands

* `python scripts/marp.py` - Generate presentations when front matter has `marp: true`

!!! note

    The **marp script will alter your markdown files** to add buttons at the bottom of the page for
    HTML and PDF.  If you change `marp: false`, it will cause the script to remove the links and
    the generated files.

## Project layout

    mkdocs.yml    # The configuration file.
    scripts/
        marp.py   # Scans for markdown files requiring presentations.
        encode.py # Converts the png template images to css embeddable images.
    marp/
        notebook/
            image/    # Has the png background images for presentations.
            notebook.css # The CSS file used for presentation formatting.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## Formatting

You can find great documentation on formatting content at the [mkdocs-material reference](https://squidfunk.github.io/mkdocs-material/reference/).