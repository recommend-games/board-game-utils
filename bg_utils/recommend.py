# -*- coding: utf-8 -*-

"""Recommend games."""

import logging

from itertools import islice
from typing import Generator, Iterable, Optional

import requests

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://recommend.games"


def _recommend_games(base_url: str, **params) -> Generator[dict, None, None]:

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


def recommend_games(
    base_url: str = BASE_URL,
    max_results: Optional[int] = 25,
    **params,
) -> Iterable[dict]:
    """Call to Recommend.Games."""

    results = _recommend_games(base_url=base_url, **params)
    return islice(results, max_results) if max_results else results
