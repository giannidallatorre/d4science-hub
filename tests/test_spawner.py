"""Tests for the spawner"""

from unittest.mock import MagicMock

import pytest
from d4science_hub.spawner import D4ScienceSpawner



@pytest.mark.asyncio
async def test_build_options_role():
    spawner = D4ScienceSpawner(_mock=True)
    roles = ["foo-role"]
    resources = {
        "genericResources": {
            "Resource": [
                {
                    "Profile": {
                        "Name": "ServerOption",
                        "Body": {
                            "ServerOption": {
                                "AuthId": "witoil-authid",
                                "Info": {
                                    "Name": "WITOIL Option",
                                    "Description": "desc",
                                },
                                "@default": "true",
                                "@role": "foo-role",
                            }
                        },
                    }
                }
            ]
        }
    }
    # role of user and resource matches
    server_opts, vol_opts = spawner.build_resource_options(roles, resources)
    assert "witoil-authid" in [s.get("AuthId", "") for s in server_opts]
    assert vol_opts == {}

    # role of user and resource does not match
    server_opts, vol_opts = spawner.build_resource_options([], resources)
    assert "witoil-authid" not in [s.get("AuthId", "") for s in server_opts]
    assert vol_opts == {}

    # no role in the resource
    del resources["genericResources"]["Resource"][0]["Profile"]["Body"]["ServerOption"][
        "@role"
    ]
    server_opts, vol_opts = spawner.build_resource_options([], resources)
    assert "witoil-authid" in [s.get("AuthId", "") for s in server_opts]
    assert vol_opts == {}


@pytest.mark.asyncio
async def test_custom_user_options():
    spawner = D4ScienceSpawner(_mock=True)
    user_options = MagicMock()
    spawner.custom_user_options = user_options
    await spawner.load_user_options()
    user_options.assert_called_once_with(spawner)
