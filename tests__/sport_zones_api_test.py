from playwright.sync_api import  APIRequestContext

def test_should_sports_zone_preview_displays(api_request_context: APIRequestContext) -> None:
    facilities_response = api_request_context.get("/api/facilities?count=500&page=1")
    assert facilities_response.ok

    sport_facilities = list(facilities_response.json()["items"])

    for sport_facility in sport_facilities:
        sport_zones_response = api_request_context.get(f"/api/facilities/{sport_facility['id']}/sportzones")
        assert sport_zones_response.ok

        sport_zones = list(sport_zones_response.json()["item"]['sportZones'])
        for sport_zone in sport_zones:
            try:
                thumbnail_url = sport_zone['mainPhoto']['thumbnailUrl']
            except Exception:
                assert False, f"Failed to open preview for sports zones {sport_zone['id']}"
            thumbnail_url_response = api_request_context.get(thumbnail_url)
            assert thumbnail_url_response.ok
            

  

