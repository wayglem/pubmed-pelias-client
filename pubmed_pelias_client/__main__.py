import argparse

from pubmed_pelias_client import bingMapsGeocoder
from pubmed_pelias_client.geoResult import GeoResult, Confidence

import unicodedata
import csv
import requests
import json
import re


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
                if args.verbose:
                    print(f"PMID {pmid} affiliations")
                affiliations = row[2].split(";")
                searchedAffiliation = []
                for index in range(0, len(affiliations)):
                    result: GeoResult
                    affiliation = sanitizeAffiliation(affiliations[index])
                    if args.verbose:
                        print(f"{affiliation[index]} was sanitized to {affiliation}")
                    cachedResult = next(
                        (
                            element
                            for element in searchedAffiliation
                            if element["affiliation"] == affiliation
                        ),
                        None,
                    )
                    if affiliation == "nowhere":
                        # A lot of record contains nowhere just ignore them
                        result = GeoResult(
                            pmid, affiliation, 0, 0, Confidence.NO_RESULT, index
                        )
                    elif cachedResult != None:
                        result = cachedResult["result"]
                    else:
                        result: GeoResult = bingGeocoder.geocode(
                            pmid, affiliation, index
                        )
                        searchedAffiliation.append(
                            {"affiliation": affiliation, "result": result}
                        )
                        outputWriter.writerow(
                            [
                                result.pmid,
                                result.affiliation,
                                result.affiliationIndex,
                                result.lat,
                                result.lng,
                                result.confidence.value,
                            ]
                        )
                        if args.verbose:
                            print(f"{affiliation} geocodeResult = {result}")
                # return  # uncomment for testing only one.

    print("Finished reading input file")


def sanitizeAffiliation(affiliation: str) -> str:
    affiliation = (
        unicodedata.normalize("NFD", affiliation)
        .encode("ascii", "ignore")
        .decode("ascii")
    )  # "transform" non ascii chars to ascii
    affiliation = affiliation.lower()  # lower case
    affiliation = re.sub(
        "[^A-Za-z0-9]+", " ", affiliation
    )  # remove all non alphanumerical chars
    affiliation = affiliation.strip()  # remove whitespaces
    return affiliation


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
