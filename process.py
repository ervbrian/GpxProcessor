import argparse
import os

from utils.backend import HikeDBClient, update_db
from utils.gpx_import import GpxImport
from utils.report import render_html, plot_elevation


GPX = "GPX"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", help="list of files to process")
    parser.add_argument("-r", "--render_only", action="store_true", default=False, help="render html only")
    return parser.parse_args()


def main():
    args = parse_args()
    client = HikeDBClient()

    if not args.render_only:
        file_list = [filename for filename in os.listdir(args.path) if filename.endswith(GPX)]
        print(f"Found {len(file_list)} GPX files in path...")

        file_list = client.filter_populated_hikes(file_list)

        print(f"Processing {len(file_list)} files after removing hikes already populated in HikeDB")
        hike_list = []
        for filename in file_list:
            print(f"Processing {filename}")
            processed_gpx = GpxImport(filename=os.path.join(args.path, filename))
            hike_list.append(processed_gpx.hike)
            plot_elevation(filename=f"{processed_gpx.name}.png", coordinates=processed_gpx.coordinates)
        update_db(client=client, hikes=hike_list)
        print(f"Total hikes stored in HikeDB database: {client.entry_count}")

    render_html(hikes=client.show_all())
    print("Generated HTML page: html/index.html")


if __name__ == "__main__":
    main()