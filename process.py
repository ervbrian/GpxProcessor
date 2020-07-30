import argparse
import os
from multiprocessing.pool import ThreadPool

from utils.backend import HikeDBClient, update_db
from utils.combine_gpx import CombineGpx
from utils.gpx_import import GpxImport
from utils.plotting import plot_elevation, plot_coordinates, plot_heart_rate
from utils.report import render_html


GPX = "GPX"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", help="list of files to process")
    parser.add_argument("-r", "--render_only", action="store_true", default=False, help="render html only")
    parser.add_argument("-c", "--combine", action="store", nargs='+', required=False, help="list of input files to combine")
    return parser.parse_args()


def main():
    args = parse_args()
    client = HikeDBClient()

    # TODO Separate processing logic into separate methods
    if not args.render_only:
        file_list = [filename for filename in os.listdir(args.path) if filename.endswith(GPX)]
        print(f"Found {len(file_list)} GPX files in path...")

        if args.combine:
            print(f"Combining the following: {args.combine}")
            full_paths = [f"{args.path}{filename}" for filename in args.combine]
            combined_filename = os.path.join(f"{args.combine[0]}_combined.GPX")
            CombineGpx(gpx_files=full_paths).write_to_file(args.path + combined_filename)
            file_list.append(combined_filename)

            for file in args.combine:
                file_list.remove(file)
                print(f"Removed {file} from processing in favor of {combined_filename}")

        file_list = client.filter_populated_hikes(file_list)

        print(f"Processing {len(file_list)} files after removing hikes already populated in HikeDB")
        hike_list = []
        for filename in file_list:
            print(f"Processing {filename}")
            processed_gpx = GpxImport(filename=os.path.join(args.path, filename))
            hike_list.append(processed_gpx.hike)

        print("Generating plot graphs")
        for hike in hike_list:
            plot_elevation(hike)
            plot_coordinates(hike)
            plot_heart_rate(hike)

        print("Populating database")
        update_db(client=client, hikes=hike_list)
        print(f"Total hikes stored in HikeDB database: {client.entry_count}")

    render_html(hikes=client.show_all_hikes())
    print("Generated HTML page: html/index.html")


if __name__ == "__main__":
    main()
