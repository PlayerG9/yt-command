#!/usr/bin/python3
r"""
download the mp3 part of a YouTube-Video
produces mp3-file including
- title
- creator
- cover/thumbnail
- lyrics
"""
import logging
import traceback
import tempfile
import sys
import os
import os.path as path
import re

import pytube.exceptions
from pytube import YouTube
from progressbar import ProgressBar
import requests

from .lyricfetcher import find_lyrics, LyricsNotFound


COMMAND_NAME = "download"


def initialise(helper: 'argparse.ArgumentParser', commands: dict):  # noqa
    import argparse

    short, description = __doc__.strip().split('\n', 1)

    parser: argparse.ArgumentParser = helper.add_parser(
        COMMAND_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=short,  # short help in main-help
        description=description  # long help in command-help
    )

    parser.add_argument('url')

    commands[COMMAND_NAME] = execute


def execute(arguments):
    Downloader(url=arguments.url, args=arguments).execute()


class Downloader:
    mp4path: str
    mp3path: str
    youtube: YouTube
    creator: str
    title: str

    def __init__(self, url: str, args):
        self.url = complete_url(url)
        self.config = args

    def execute(self) -> None:
        try:
            self.findAndValidate()
            self.collectMetadata()
            self.downloadAudio()
            self.convertFileFormat()
            self.manipulateMetadata()
        except Exception as exception:
            mp3path = getattr(self, 'mp3path', None)
            if mp3path and path.isfile(mp3path):
                os.remove(mp3path)
            raise exception

    def findAndValidate(self) -> None:
        logging.info("Searching for Video...")

        youtube = YouTube(self.url)

        print("Title: ", youtube.title)
        print("Author:", youtube.author)
        print("Views: ", "{:,}".format(youtube.views))
        print("Length:", f"{youtube.length // 60}:{youtube.length % 60}")

        if input("Proceed? (y) ").lower() != 'y':
            sys.exit(0)

        self.youtube = youtube

    def collectMetadata(self) -> None:
        title = self.youtube.title
        author = self.youtube.author

        title = removeBrackets(title)

        left, sep, right = title.partition('-')
        if not sep:  # - is not the seperator
            left = title
            right = author

        left = removeNonUnicode(left)
        right = removeNonUnicode(right)

        print("(1) Title={!r:<25} Creator={!r:<20}".format(left, right))
        print("(2) Title={!r:<25} Creator={!r:<20}".format(right, left))
        print("(3) Manuel Input")

        while True:
            try:
                a = int(input("> "))
            except ValueError:
                logging.warning("invalid input")
            else:
                break

        if a == 1:
            self.title = left
            self.creator = right
        elif a == 2:
            self.title = right
            self.creator = left
        elif a == 3:
            self.title = input("Title: ")
            self.creator = input("Creator: ")
        else:
            raise ValueError("invalid input")

        self.mp3path = path.abspath(fix4filename(f"{self.creator}_{self.title}") + '.mp3')
        logging.debug(f"mp3 path generated ({self.mp3path}")

    def downloadAudio(self) -> None:
        @self.youtube.register_on_progress_callback
        def on_progress(_, __, bytes_remaining: int):
            pgb.update(stream.filesize - bytes_remaining)

        logging.debug("Searching for download...")
        try:
            stream = self.youtube.streams.get_audio_only()
        except pytube.exceptions.PytubeError:
            raise RuntimeError("Failed to find audio-download")

        logging.info(f"Found download with audio-quality of {stream.bitrate // 1000}k")
        logging.debug("Downloading...")
        file_config = dict(
            output_path=tempfile.gettempdir(),
            filename='yt-only-audio.mp4'
        )
        self.mp4path = stream.get_file_path(**file_config)
        logging.debug(f"mp3 path generated ({self.mp4path}")
        pgb = ProgressBar(maxval=stream.filesize).start()
        stream.download(**file_config, skip_existing=False)
        pgb.finish()

    def download_thumbnail(self) -> (bytes, str):
        import mimetypes

        mimetype: str = mimetypes.guess_type(self.youtube.thumbnail_url)[0]
        logging.debug(f"downloading thumbnail ({self.youtube.thumbnail_url}|{mimetype})")
        response = requests.get(self.youtube.thumbnail_url)
        response.raise_for_status()
        logging.debug("thumbnail successfully downloaded")

        return response.content, mimetype

    def convertFileFormat(self) -> None:
        from moviepy.editor import AudioFileClip

        logging.debug("loading mp4-file")
        clip = AudioFileClip(self.mp4path)
        # verbose = info & logger = progress-bar
        # clip.write_audiofile(self.mp3path, verbose=False, logger=None)
        logging.info("writing mp3-file")
        clip.write_audiofile(self.mp3path, verbose=False)

    def manipulateMetadata(self) -> None:
        import eyed3.mp3
        from eyed3.id3.frames import ImageFrame

        audiofile: eyed3.core.AudioFile = eyed3.load(self.mp3path)
        if audiofile.tag is None:
            audiofile.initTag()
        tag: eyed3.mp3.id3.Tag = audiofile.tag

        tag.title = self.title
        tag.artist = self.creator

        logging.info("Fetching Thumbnail...")
        try:
            blob, mimetype = self.download_thumbnail()
        except (requests.Timeout, requests.HTTPError) as error:
            logging.warning("Failed to fetch thumbnail")
            logging.warning(f"({error.__class__.__name__}: {error})")
            if self.config.debug:
                traceback.print_exception(None, error, error.__traceback__)
        else:
            # for keyId in [ImageFrame.ICON, ImageFrame.FRONT_COVER]:
            tag.images.set(
                ImageFrame.FRONT_COVER,
                blob,
                mimetype
            )

        logging.info("Fetching Lyrics...")
        try:
            lyrics: str = find_lyrics(self.title, self.creator)
        except (requests.Timeout, requests.HTTPError, LyricsNotFound) as error:
            logging.warning("Failed to fetch lyrics")
            logging.warning(f"({error.__class__.__name__}: {error})")
            if self.config.debug:
                traceback.print_exception(None, error, error.__traceback__)
        else:
            tag.lyrics.set(lyrics)

        logging.info("Updating metadata...")
        try:
            tag.save()
        except eyed3.Error:
            logging.warning("Failed to update metadata")


def fix4filename(filename: str) -> str:
    filename = re.sub(r'[^\w\-.()]', '_', filename).strip()
    while '__' in filename:
        filename = filename.replace('__', '_')
    return filename


def removeBrackets(string: str) -> str:
    return re.sub(r"\(.+\)|\[.+]", lambda m: "", string).strip()  # remove everything within brackets


def removeNonUnicode(string: str) -> str:
    return re.sub(r'[^\w\- \'!?]', '', string).strip()  # remove non-word-characters


def complete_url(known: str) -> str:
    r"""
    allowed formats
    {ID}
    v={ID}
    /watch?v={ID}
    https://youtube.com/watch?v={ID}
    """
    if known.startswith("https://"):
        return f"{known}"
    elif known.startswith("/watch?v="):
        return f"https://youtube.com{known}"
    elif known.startswith("v="):
        return f"https://youtube.com/watch?{known}"
    else:
        return f"https://youtube.com/watch?v={known}"
