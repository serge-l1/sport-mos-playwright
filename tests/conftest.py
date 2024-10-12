from typing import Generator
from dotenv import dotenv_values
import pytest
from playwright.sync_api import Playwright, APIRequestContext

config = dotenv_values()


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url=config['BASE_URL']
    )
    yield request_context
    request_context.dispose()
