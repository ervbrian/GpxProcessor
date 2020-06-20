import matplotlib.pyplot as plt
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


def plot_elevation(filename, coordinates):
    """ Generate a plot graph of elevation values for a list coordinates

    :param filename: string
    :param coordinates: list of Point objects
    :return: None
    """

    fig, ax = plt.subplots(1)
    ax.plot([point.elevation for point in coordinates[1:]])
    plt.title(filename)
    plt.xlabel("Coordinate")
    plt.ylabel("Elevation(m)")
    plt.style.use(['dark_background'])
    plt.savefig(f"images/{filename}")
