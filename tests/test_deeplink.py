import pytest

from affo_deeplink import settings


@pytest.mark.parametrize("deeplink_id", ["", "123", "test", "ава"])
async def test_deeplink_wrong_id(client, deeplink_id):
    resp = await client.get(f"/{deeplink_id}")
    assert resp.status == 404


@pytest.mark.parametrize("deeplink_data", [{}])
async def test_deeplink_no_url(app, client, deeplink_data):
    deeplink_id = app["deeplink_s"].dumps(deeplink_data)

    resp = await client.get(f"/{deeplink_id}")
    assert resp.status == 404


@pytest.mark.freeze_time("2019-01-01")
@pytest.mark.parametrize(
    "deeplink_data,event_data",
    [
        (
            {"url": "http://example.com"},
            {
                "cf1": None,
                "cf2": None,
                "cf3": None,
                "cf4": None,
                "cf5": None,
                "cid": "00000000000000000000000000000000",
                "cn": None,
                "dl": "http://example.com",
                "dr": None,
                "t": "pageview",
                "tid": None,
                "uip": "127.0.0.1",
                "utt": "2019-01-01 00:00:00",
                "uua": None,
            },
        ),
        (
            {"tracking_id": "woohoo", "url": "http://example.com"},
            {
                "cf1": None,
                "cf2": None,
                "cf3": None,
                "cf4": None,
                "cf5": None,
                "cid": "00000000000000000000000000000000",
                "cn": None,
                "dl": "http://example.com",
                "dr": None,
                "t": "pageview",
                "tid": "woohoo",
                "uip": "127.0.0.1",
                "utt": "2019-01-01 00:00:00",
                "uua": None,
            },
        ),
        (
            {"tracking_id": "woohoo", "campaign_name": "blackfriday", "url": "http://example.com"},
            {
                "cf1": None,
                "cf2": None,
                "cf3": None,
                "cf4": None,
                "cf5": None,
                "cid": "00000000000000000000000000000000",
                "cn": "blackfriday",
                "dl": "http://example.com",
                "dr": None,
                "t": "pageview",
                "tid": "woohoo",
                "uip": "127.0.0.1",
                "utt": "2019-01-01 00:00:00",
                "uua": None,
            },
        ),
    ],
)
async def test_deeplink_redirect(
    app, client, deeplink_data, event_data, mock_client_session, mock_uuid,
):
    deeplink_id = app["deeplink_s"].dumps(deeplink_data)

    resp = await client.get(f"/{deeplink_id}", allow_redirects=False)
    assert resp.status == 302
    mock_client_session.assert_called_once_with(
        f"{settings.EVENTS_API_URL}/event/", json=event_data,
    )
