import argparse

from . import BaseClass, base_function  # pragma: no cover
import csv
import requests


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m pubmed_pelias_client` and `$ pubmed_pelias_client `.

    """
    parser = argparse.ArgumentParser(
        description="pubmed_pelias_client.",
        epilog="Enjoy the pubmed_pelias_client functionality!",
    )
    # This is required positional argument
    parser.add_argument(
        "inputFile",
        type=str,
        help="Path to the input file",
        default="/tmp/data/data.csv",
    )
    # This is optional named argument
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Optionally adds verbosity",
    )
    args = parser.parse_args()
    print(f"reading {args.inputFile}!")
    if args.verbose:
        print("Verbose mode is on.")

    print("Executing main function")
    # base = BaseClass()
    # print(base.base_method())
    # print(base_function())
    # TODO: create cache
    with open(args.inputFile, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            print(f"PMID {row[1]} affiliations")
            affiliations = row[2].split(";")
            for affiliation in affiliations:
                # TODO: check that spaces are parsed correctly (dumb server is logging "+" chars between words)
                payload = {"text": affiliation}
                r = requests.get("http://localhost:4000/v1/search?", params=payload)
                # TODO: handle error cases
                if r.status_code == 200:
                    responseJson = r.json()
                    if (
                        responseJson["features"][0]["type"] == "Feature"
                        and responseJson["features"][0]["geometry"]["type"] == "Point"
                    ):
                        lat = responseJson["features"][0]["geometry"]["coordinates"][0]
                        lon = responseJson["features"][0]["geometry"]["coordinates"][1]
                        print(f"\t {affiliation}: [{lat}, {lon}]")
                    else:
                        print(
                            f"Failed to parse JSON for affiliation=[{affiliation}]. Json=[{responseJson}]"
                        )
                else:
                    print(
                        f"Request to geocode failed for affiliation=[{affiliation}]. status=[{r.status_code}]"
                    )
    print("End of main function")


if __name__ == "__main__":  # pragma: no cover
    main()
