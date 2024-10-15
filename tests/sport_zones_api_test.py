from playwright.sync_api import  APIRequestContext

def test_should_sports_zone_preview_displays(api_request_context: APIRequestContext) -> None:
    facilities_response = api_request_context.get("/api/facilities?count=5000&page=1")
    assert facilities_response.ok

    sport_facilities = list(facilities_response.json()["items"])

    errors = []
    
    for sport_facility in sport_facilities:
        sport_zones_response = api_request_context.get(f"/api/facilities/{sport_facility['id']}/sportzones")
        assert sport_zones_response.ok

        sport_zones = list(sport_zones_response.json()["item"]['sportZones'])
       
        for sport_zone in sport_zones:
            try:
                photo_url = sport_zone['mainPhoto']['url']
            except:
                print(f"Failed to open photo for sports zones {sport_facility['id']}")
                errors.append(sport_facility['id'])
                continue
            photo_url_response = api_request_context.get(photo_url)
            assert photo_url_response.ok
           
            if(photo_url_response.body() == b''):
                print(f"Downloaded file is empty for sports zones {sport_facility['id']} img link: {photo_url}")
                errors.append(sport_facility['id'])

    assert errors == []

  

