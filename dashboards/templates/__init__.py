from pathlib import Path

from jinja2 import Template


def tpl(name: str):
    return Template((Path(__file__).parent / (name + ".html")).read_text())

page = tpl("page")