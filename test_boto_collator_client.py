import pytest
from boto3 import Session
from botocore.stub import Stubber

from boto_collator_client import CollatorClient


@pytest.fixture()
def iam_client(request):
    """Stubs the list_users method, a paginated API."""

    response_factory = request.param
    api, responses = response_factory()

    iam = Session().client("iam")
    stubber = Stubber(iam)

    for response in responses:
        stubber.add_response(api, response)

    with stubber:
        yield iam


def list_users_stubs():
    """Stubs for the list_users method, a paginated API."""

    return (
        "list_users",
        [
            {
                "Users": [
                    {
                        "UserName": "User1",
                        "UserId": "Id11111111111111",
                        "CreateDate": "2022-02-08",
                        "Path": "/",
                        "Arn": "Arn111111111111111111111",
                    }
                ],
                "IsTruncated": True,
                "Marker": "Page1",
            },
            {
                "Users": [
                    {
                        "UserName": "User2",
                        "UserId": "Id22222222222222",
                        "CreateDate": "2022-02-08",
                        "Path": "/",
                        "Arn": "Arn222222222222222222222",
                    }
                ],
                "IsTruncated": False,
                "Marker": "Page2",
            },
        ],
    )


def list_open_id_connect_providers_stubs():
    """Stubs for the list_open_id_connect_providers method, an unpaginated API."""

    return (
        "list_open_id_connect_providers",
        [{"OpenIDConnectProviderList": [{"Arn": "Arn11111111111111111"}]}],
    )


@pytest.mark.parametrize("iam_client", [pytest.param(list_users_stubs)], indirect=True)
def test_boto3_client_gets_first_page_only(iam_client):
    response = iam_client.list_users()
    assert [u["UserName"] for u in response["Users"]] == ["User1"]


@pytest.mark.parametrize("iam_client", [pytest.param(list_users_stubs)], indirect=True)
def test_collator_gets_all_pages(iam_client):
    cc = CollatorClient(iam_client)
    response = cc.list_users()
    assert [u["UserName"] for u in response["Users"]] == ["User1", "User2"]


@pytest.mark.parametrize(
    "iam_client",
    [pytest.param(list_open_id_connect_providers_stubs)],
    indirect=True,
)
def test_collator_gets_unpaginated(iam_client):
    cc = CollatorClient(iam_client)
    response = cc.list_open_id_connect_providers()
    assert [p["Arn"] for p in response["OpenIDConnectProviderList"]] == [
        "Arn11111111111111111"
    ]
