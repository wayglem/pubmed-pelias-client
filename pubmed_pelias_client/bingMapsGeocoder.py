import requests

from pubmed_pelias_client.geoResult import Confidence, GeoResult


class BingMapsGeocoder:
    def __init__(self, key) -> None:
        self.key = key

    def search(self, locationName, maxResults=1) -> str:
        baseUrl = "http://dev.virtualearth.net/REST/v1/Locations"
        query = {
            "query": locationName,
            "includeNeighborhood": 0,
            "include": "queryParse,ciso2",
            "maxResults": maxResults,
            "key": self.key,
        }
        r = requests.get(baseUrl, params=query)
        if r.status_code == 200:
            return r.json()
        else:
            print(
                f"ERROR: geocode request failed for location {locationName} with status code {r.status_code}"
            )
            return "Failed to find location with status " + str(r.status_code)

    def parse(self, jsonResponse, pmid: str, affiliation: str, index: int) -> GeoResult:
        confidence = Confidence.UNSPECIFIED
        if (
            "resourceSets" in jsonResponse
            and len(jsonResponse["resourceSets"]) > 0
            and "resources" in jsonResponse["resourceSets"][0]
            and len(jsonResponse["resourceSets"][0]["resources"]) > 0
            and "point" in jsonResponse["resourceSets"][0]["resources"][0]
            and "coordinates"
            in jsonResponse["resourceSets"][0]["resources"][0]["point"]
        ):
            if "confidence" in jsonResponse["resourceSets"][0]["resources"][0]:
                confidence = convertToConfidence(
                    jsonResponse["resourceSets"][0]["resources"][0]["confidence"]
                )
            return GeoResult(
                pmid,
                affiliation,
                jsonResponse["resourceSets"][0]["resources"][0]["point"]["coordinates"][
                    0
                ],
                jsonResponse["resourceSets"][0]["resources"][0]["point"]["coordinates"][
                    1
                ],
                confidence,
                index,
            )
        else:
            return GeoResult(pmid, affiliation, 0, 0, Confidence.NO_RESULT, index)

    def geocode(self, pmid, affiliation, index) -> GeoResult:
        json = self.search(affiliation)
        return self.parse(json, pmid, affiliation, index)


def convertToConfidence(x: str) -> Confidence:
    return {
        "High": Confidence.HIGH,
        "Medium": Confidence.MEDIUM,
        "Low": Confidence.LOW,
    }.get(x, Confidence.UNSPECIFIED)
