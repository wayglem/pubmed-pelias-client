import argparse

from pubmed_pelias_client import bingMapsGeocoder
from pubmed_pelias_client.geoResult import GeoResult

import csv
import requests
import json


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m pubmed_pelias_client` and `$ pubmed_pelias_client `.

    """
    parser = argparse.ArgumentParser(
        description="pubmed_pelias_client.",
        epilog="Enjoy the pubmed_pelias_client functionality!",
    )
    parser.add_argument(
        "--bing_key",
        required=True,
        type=str,
        help="api_key for bing API",
    )
    parser.add_argument(
        "--geocode_earth_key",
        required=False,
        type=str,
        help="api_key for api.geocode.earth",
        default="ge-xxx",
    )
    parser.add_argument(
        "--output_file",
        required=False,
        type=str,
        help="path for csv outputfile",
        default="output.csv",
    )
    parser.add_argument(
        "inputFile",
        type=str,
        help="Path to the input file",
        default="/tmp/data/data.csv",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Optionally adds verbosity",
    )
    args = parser.parse_args()
    print(f"reading {args.inputFile}!")
    bingKey = args.bing_key
    # geocodeEarthKey = args.geocode_earth_key

    outputFile = args.output_file

    if args.verbose:
        print("Verbose mode is on.")

    print("Start reading file")
    with open(outputFile, "w", newline="") as csvfile:
        outputWriter = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
        outputWriter.writerow(
            ["PMID", "affiliation", "affiliation_index", "lat", "lng", "confidence"]
        )
        with open(args.inputFile, newline="") as csvfile:
            bingGeocoder = bingMapsGeocoder.BingMapsGeocoder(bingKey)
            inputFileReader = csv.reader(csvfile, delimiter=",")

            for row in inputFileReader:
                pmid = row[1]
                print(f"PMID {pmid} affiliations")
                affiliations = row[2].split(";")
                index = 0  # FIXME: currently only parsing first affiliation
                affiliation = affiliations[index]
                if affiliation.lower() == "nowhere":
                    # A lot of record contains nowhere just ignore them FIXME: better handling is required
                    continue
                result: GeoResult = bingGeocoder.geocode(pmid, affiliation, index)
                outputWriter.writerow(
                    [
                        result.pmid,
                        result.affiliation,
                        result.affiliationIndex,
                        result.lat,
                        result.lng,
                        result.confidence,
                    ]
                )
                print(f"{affiliation} geocodeResult = {result}")
                # return  # uncomment for testing only one.

    print("End of main function")


def call_pelias(
    affiliation, key
):  # used before to call local pelias or geocode.earth. DEAD CODE
    payload = {"text": affiliation, "api_key": key}
    # r = requests.get("http://localhost:4000/v1/search?", params=payload)
    r = requests.get("https://api.geocode.earth/v1/search?", params=payload)
    if r.status_code == 200:
        responseJson = r.json()
        if (
            "features" in responseJson
            and len(responseJson["features"]) > 0
            and responseJson["features"][0]["type"] == "Feature"
            and responseJson["features"][0]["geometry"]["type"] == "Point"
        ):
            lat = responseJson["features"][0]["geometry"]["coordinates"][0]
            lon = responseJson["features"][0]["geometry"]["coordinates"][1]
            print(f"\t {affiliation}: [{lon}, {lat}]")
            print(json.dumps(responseJson, indent=4, sort_keys=True))
        elif len(responseJson["features"]) == 0:
            print(f"NO_RESULTS=[{affiliation}].")
        else:
            print(
                f"Failed to parse JSON for affiliation=[{affiliation}]. Json=[{responseJson}]"
            )
    else:
        print(
            f"Request to geocode failed for affiliation=[{affiliation}]. status=[{r.status_code}]"
        )


if __name__ == "__main__":  # pragma: no cover
    main()
