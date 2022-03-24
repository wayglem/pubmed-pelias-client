import pytest
import json
from pubmed_pelias_client import bingMapsGeocoder
from pubmed_pelias_client.geoResult import Confidence, GeoResult


def test_parser():
    bing = bingMapsGeocoder.BingMapsGeocoder("key")
    exampleBingResponse = json.loads(
        '{"authenticationResultCode":"ValidCredentials","brandLogoUri":"http://dev.virtualearth.net/Branding/logo_powered_by.png","copyright":"Copyright Â© 2014 Microsoft and its suppliers. All rights reserved. This API cannot be accessed and the content and any results may not be used, reproduced or transmitted in any manner without express written permission from Microsoft Corporation.","resourceSets":[{"estimatedTotal":1,"resources":[{"__type":"Location:http://schemas.microsoft.com/search/local/ws/rest/v1","bbox":[51.507022857666016,-0.078029103577137,51.50926971435547,-0.07442080229520798],"name":"Tower of London, United Kingdom","point":{"type":"Point","coordinates":[51.509521484375,-0.0763700008392334]},"address":{"adminDistrict":"England","adminDistrict2":"London","countryRegion":"United Kingdom","formattedAddress":"Tower of London, United Kingdom","locality":"London","neighborhood":"EC3","landmark":"Tower of London"},"confidence":"High","entityType":"HistoricalSite","geocodePoints":[{"type":"Point","coordinates":[51.509521484375,-0.0763700008392334],"calculationMethod":"Rooftop","usageTypes":["Display"]}],"matchCodes":["Good"]}]}],"statusCode":200,"statusDescription":"OK","traceId":"b0a6385e511b409aaeddd4be7c2ffaed"}'
    )
    geocode: GeoResult = bing.parse(
        exampleBingResponse, "example_id", "expected_affiliation", 1
    )
    assert geocode.confidence == Confidence.HIGH
    assert geocode.lat == 51.509521484375
    assert geocode.lng == -0.0763700008392334
    assert geocode.affiliationIndex == 1
    assert geocode.affiliation == "expected_affiliation"
