#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
maybe utilize the search function for better results
the current way of creating the url is not perfect
"""
import logging

import requests
from bs4 import BeautifulSoup
from bs4 import element as html_elements


class LyricsNotFound(LookupError):
    pass


def find_lyrics(title: str, creator: str) -> str:
    logging.debug(f"starting search for lyrics ({creator}: {title})")
    url = search_for_lyrics(title, creator)
    logging.debug(f"found lyrics url ({url})")
    return fetch_lyrics(url)


def search_for_lyrics(title: str, creator: str) -> str:
    from urllib.parse import quote_plus

    provider = "https://search.azlyrics.com"

    query = f"{creator} {title}"
    url = f"{provider}/search.php?w=songs&p=1&q=" + quote_plus(query)
    logging.debug(f"query url generated ({url})")

    response = requests.get(url)
    response.raise_for_status()
    logging.debug("request successful")

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find("table")

    # search can fail without status-code of 404 (still 200)
    if table is None:
        raise LyricsNotFound("just not found")

    lyrics_url = table.find("a").get('href')

    if not lyrics_url or not lyrics_url.startswith(provider):
        raise LyricsNotFound("something went wrong in the search")

    return lyrics_url


def fetch_lyrics(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    element = soup.find(text=find_lyrics_container).parent
    if not element:
        raise LookupError("failed to extract the lyrics")
    logging.debug("lyrics container found")

    # don't use string with += because that's worse (and slower)
    lyrics_lines = []

    for child in element.childGenerator():
        if not isinstance(child, html_elements.NavigableString):
            continue
        lyrics_lines.append(child.text)

    # the lines already contain a linebreak
    # PS. I don't really remember why there is a .strip() but I think it was important
    return ''.join(lyrics_lines).strip()


def find_lyrics_container(text) -> bool:
    # There is a comment parallel to the lyrics with the following content:
    # Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. ...
    # shortened 'third-party' is sufficient to check
    return isinstance(text, html_elements.Comment) and 'third-party' in text


if __name__ == '__main__':
    print(find_lyrics("discord", ""))
