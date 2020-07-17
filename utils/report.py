from jinja2 import Environment, FileSystemLoader
import os


def render_html(hikes):
    """ Given a list of hikes, render an HTML report based on Jinja templates

    :param hikes: list of HikeDB objects
    :return: None
    """

    templates_dir = "templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("hike.html")

    filename = os.path.join("html", "index.html")
    with open(filename, "w") as fh:
        fh.write(template.render(hikes=hikes))
