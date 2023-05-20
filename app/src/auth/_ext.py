from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("Weggo"),
    autoescape=select_autoescape()
)