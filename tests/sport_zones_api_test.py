from playwright.sync_api import APIRequestContext

def test_should_sports_zone_preview_displays(api_request_context: APIRequestContext) -> None:
    # Получаем список спортивных объектов
    facilities_response = api_request_context.get("/api/facilities?count=4770&page=1")
    assert facilities_response.ok

    sport_facilities = list(facilities_response.json()["items"])

    errors = []

    for sport_facility in sport_facilities:
        facility_id = sport_facility.get('id')  # Получаем id спортобъекта
        
        # Запрашиваем спортивные зоны для каждого спортивного объекта
        sport_zones_response = api_request_context.get(f"/api/facilities/{facility_id}/sportzones")
        assert sport_zones_response.ok

        sport_zones = list(sport_zones_response.json()["item"]['sportZones'])

        for sport_zone in sport_zones:
            try:
                # Попытка получить URL изображения превью
                thumbnail_url = sport_zone['mainPhoto']['thumbnailUrl']
                thumbnail_url_response = api_request_context.get(thumbnail_url)
                assert thumbnail_url_response.ok
            except Exception:
                print(f"Failed to open preview for sports zone. facilityId: {facility_id}, externalId: {sport_facility.get('externalId')}, name: {sport_facility.get('name')}")
                errors.append(f"facilityId: {facility_id}, externalId: {sport_facility.get('externalId')} - {sport_facility.get('name')}")
                continue

            # Попытка получить основной URL изображения
            try:
                photo_url = sport_zone['mainPhoto']['url']
                photo_url_response = api_request_context.get(photo_url)
                assert photo_url_response.ok

                if photo_url_response.body() == b'':
                    print(f"Downloaded file is empty for sports zone. facilityId: {facility_id}, externalId: {sport_facility.get('externalId')}, name: {sport_facility.get('name')} img link: {photo_url}")
                    errors.append(f"facilityId: {facility_id}, externalId: {sport_facility.get('externalId')} - {sport_facility.get('name')}")

            except Exception:
                print(f"Failed to open photo for sports zone. facilityId: {facility_id}, externalId: {sport_facility.get('externalId')}, name: {sport_facility.get('name')}")
                errors.append(f"facilityId: {facility_id}, externalId: {sport_facility.get('externalId')} - {sport_facility.get('name')}")
                continue

    assert errors == []