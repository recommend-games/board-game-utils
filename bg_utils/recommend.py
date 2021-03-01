# -*- coding: utf-8 -*-

"""Recommend games."""

import logging

import requests

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://recommend.games"


def recommend_games(base_url=BASE_URL, **params):
    """Call to Recommend.Games."""

    url = f"{base_url}/api/games/recommend/"
    params.setdefault("page", 1)

    while True:
        LOGGER.info("Requesting page %d", params["page"])

        try:
            response = requests.get(url, params)
        except Exception:
            LOGGER.exception(
                "Unable to retrieve recommendations with params: %r", params
            )
            return

        if not response.ok:
            LOGGER.error("Request unsuccessful: %s", response.text)
            return

        try:
            result = response.json()
        except Exception:
            LOGGER.exception("Invalid response: %s", response.text)
            return

        if not result.get("results"):
            return

        yield from result["results"]

        if not result.get("next"):
            return

        params["page"] += 1