#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
maybe utilize the search function for better results
the current way of creating the url is not perfect
"""
import requests
from bs4 import BeautifulSoup
from bs4 import element as html_elements


def find_lyrics(title: str, creator: str) -> str:
    url = f"https://www.azlyrics.com/lyrics/{fix_url_param(creator)}/{fix_url_param(title)}.html"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    element = soup.find(text=find_lyrics_container).parent
    if not element:
        raise LookupError()
    lyrics = []

    for child in element.childGenerator():
        if not isinstance(child, html_elements.NavigableString):
            continue
        lyrics.append(child.text)

    return ''.join(lyrics).strip()


def find_lyrics_container(text):
    # There is a comment with the following content:
    # Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. ...
    return isinstance(text, html_elements.Comment) and 'third-party' in text


def fix_url_param(string: str) -> str:
    import re
    return re.sub(r'\W', "", string.lower())  # remove spaces and make lowercase


if __name__ == '__main__':
    print(find_lyrics("Valerie", "Amy Winehouse"))
