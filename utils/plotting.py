import matplotlib.pyplot as plt


def plot_elevation(hike):
    """ Generate a plot graph of elevation vs distance travelled
    :return: None
    """

    fig, ax = plt.subplots(1)
    for segment in hike.segments:
        ax.plot([point.distance_from_start for point in segment.points[:-1]],
                [point.elevation for point in segment.points[:-1]])
    plt.title(hike.name)
    plt.xlabel("Distance(km)")
    plt.ylabel("Elevation(m)")
    plt.style.use(['dark_background'])
    plt.savefig(f"images/{hike.name}.png")
    plt.close()


def plot_coordinates(hike):
    """ Generate a plot graph of latitude and longitude coordinates
    :return: None
    """

    fig, ax = plt.subplots(1)
    for segment in hike.segments:
        ax.plot([point.lon for point in segment.points],
                [point.lat for point in segment.points])
    plt.title(hike.name)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.style.use(['dark_background'])
    plt.savefig(f"images/{hike.name}_coordinates.png")
    plt.close()
