import uuid

from aiohttp import web

import asynctest

import pytest

from affo_deeplink.main import init_app


@pytest.fixture()
def app():
    return init_app()


@pytest.fixture()
async def client(aiohttp_client, app):
    return await aiohttp_client(app, skip_auto_headers=["User-Agent"])


@pytest.fixture()
def mock_client_session(app):
    with asynctest.patch.object(
        app["client_session"], "post", asynctest.CoroutineMock(return_value=web.Response())
    ) as mock_:
        yield mock_


@pytest.fixture()
def mock_uuid():
    with asynctest.patch("uuid.uuid4", return_value=uuid.UUID("00000000-0000-0000-0000-000000000000")) as mock_:
        yield mock_
