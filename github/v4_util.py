# ------------------------------------------------------------- #
#                 Obliging Ode & Unsung Anthem
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""
This support module has helpers for the GitHub API v4.
"""

import json
import os

import requests

from support import data

from support.defaults import GITHUB_API_V4_ENDPOINT

from support.variables import ODE_GRAPHQL_ROOT

from util import diagnostics


def get_github_version(component, github_data):
    """Concatenate the full version for GitHub."""
    if github_data.version_prefix:
        ret = "{}{}".format(github_data.version_prefix, component.version)
    else:
        ret = component.version
    return ret


def call_query(file_name, replacements=None):
    """Calls the given GraphQL query."""
    with open(os.path.join(ODE_GRAPHQL_ROOT, file_name)) as query_file:
        raw_query = str(query_file.read())
    if replacements:
        for k, v in replacements.items():
            raw_query = raw_query.replace(k, v)
    diagnostics.trace("Calling the following GraphQL query:\n{}".format(
        raw_query))
    query = json.dumps({"query": raw_query})
    response = requests.post(
        url=GITHUB_API_V4_ENDPOINT,
        data=query,
        headers={
            "User-Agent": "anttikivi", "Accept": "application/json",
            "Authorization": "bearer {}".format(data.session.github_token)
        })

    diagnostics.trace("The response of the query was:\n{}".format(
        response.json()))

    return response.json()["data"]


def find_release_node(
        component, github_data, json_data, let_use_fallback=False):
    """
    Finds the requested release node from the GitHub API JSON
    data.
    """
    release_edges = json_data["repository"]["releases"]["edges"]
    ret_node = None
    gh_version = get_github_version(component, github_data)
    for edge in release_edges:
        node = edge["node"]
        if node is None or node["name"] == "":
            continue
        if node["name"] == gh_version:
            diagnostics.debug("Found the release {} ({}) of {}".format(
                component.version, gh_version, component.repr))
            ret_node = node

    if not ret_node and let_use_fallback:
        return release_edges[0]["node"]

    return ret_node


def find_release_node_by_tag(component, github_data, json_data):
    """
    Finds the requested release node from the GitHub API JSON
    data by the tag name.
    """
    release_edges = json_data["repository"]["releases"]["edges"]
    ret_node = None
    gh_version = get_github_version(component, github_data)
    for edge in release_edges:
        node = edge["node"]
        if node is None or node["name"] == "":
            continue
        tag_name = node["tag"]["name"]
        if tag_name == gh_version:
            diagnostics.debug("Found the release {} ({}) of {}".format(
                component.version, gh_version, component.repr))
            ret_node = node
    return ret_node
