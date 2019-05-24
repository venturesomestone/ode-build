# ------------------------------------------------------------- #
#                       Couplet Composer
# ------------------------------------------------------------- #
#
# This source file is part of the Couplet Composer project which
# is part of the Obliging Ode and Unsung Anthem projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

import json
import os

import requests

from absl import logging

from support.values import GITHUB_API_V4_ENDPOINT, GITHUB_OAUTH_TOKEN


def call_query(file, replacements=None):
    """Calls the given GraphQL query and return the raw data."""
    with open(file) as query_file:
        raw_query = str(query_file.read())
    if replacements:
        for k, v in replacements.items():
            raw_query = raw_query.replace(k, v)
    logging.debug("Calling the following GraphQL query:\n%s", raw_query)
    query = json.dumps({"query": raw_query})
    response = requests.post(
        url=GITHUB_API_V4_ENDPOINT,
        data=query,
        headers={
            "User-Agent": "anttikivi", "Accept": "application/json",
            "Authorization": "bearer {}".format(GITHUB_OAUTH_TOKEN)
        })
    logging.debug("The response of the query was:\n%s", response.json())
    return response.json()


def find_release_node(component, github_data, json_data):
    """
    Finds the requested release node from the GitHub API JSON
    data.
    """
    release_id = json_data["data"]["repository"]["release"]["id"]
    logging.debug("The utility tries to find the release ID '%s'", release_id)
    release_edges = json_data["data"]["repository"]["releases"]["edges"]
    ret_node = None
    for edge in release_edges:
        node = edge["node"]
        logging.debug("The current edge has the ID '%s'", node["id"])
        if node is None or node["id"] == "":
            continue
        if node["id"] == release_id:
            logging.debug(
                "The release of %s with the ID %s found",
                component.repr,
                release_id
            )
            ret_node = node
    return ret_node
