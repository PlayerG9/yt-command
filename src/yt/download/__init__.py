#!/usr/bin/python3
r"""
download the mp3 part of a YouTube-Video

"""
import tempfile
import sys
import os.path as path
import re

import pytube.exceptions
from pytube import YouTube
from progressbar import ProgressBar


def initialise(helper: 'argparse.ArgumentParser'):  # noqa
    import argparse

    parser: argparse.ArgumentParser = helper.add_parser(
        "download",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=__doc__.split('\n', 1)[0],  # short help in main-help
        description=__doc__  # long help in command-help
    )

    parser.add_argument('url')


def execute(arguments):
    Downloader(url=arguments.url).execute()


class Downloader:
    mp4path: str
    mp3path: str
    thumbnailData: bytes
    thumbnailMimeType: str
    youtube: YouTube
    creator: str
    title: str

    def __init__(self, url: str):
        if not url.startswith("https://"):
            if url.startswith("/watch"):
                url = "https://youtube.com"
            else:
                url = "https://youtube.com/watch?v=" + url
        self.url = url

    def execute(self):
        self.findAndValidate()
        self.collectMetadata()
        self.downloadAudio()
        self.download_thumbnail()
        self.convertFileFormat()
        self.manipulateMetadata()

    def findAndValidate(self):
        print("Searching for Video...")

        youtube = YouTube(self.url)

        print("Title: ", youtube.title)
        print("Author:", youtube.author)
        print("Views: ", "{:,}".format(youtube.views))
        print("Length:", f"{youtube.length // 60}:{youtube.length % 60}")

        if input("Proceed? (y) ") != 'y':
            sys.exit(0)

        self.youtube = youtube

    def collectMetadata(self):
        title = self.youtube.title
        author = self.youtube.author

        title = re.sub(r"\(.+\)", lambda m: "", title).strip()

        self.mp3path = path.abspath(fix_filename(title) + '.mp3')

        left, sep, right = title.partition('-')
        if not sep:  # - is not the seperator
            left = title
            right = author

        left = left.strip()
        right = right.strip()

        print("(1) Title={!r:<20} Creator={!r:<20}".format(left, right))
        print("(2) Title={!r:<20} Creator={!r:<20}".format(right, left))
        print("(3) Manuel Input")

        a = int(input("> "))

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

    def downloadAudio(self):
        @self.youtube.register_on_progress_callback
        def on_progress(_, __, bytes_remaining: int):
            pgb.update(stream.filesize - bytes_remaining)

        print("Searching for download...")
        try:
            stream = self.youtube.streams.get_audio_only()
        except pytube.exceptions.PytubeError:
            raise RuntimeError("Failed to find audio-download")

        print("Found download with audio-quality of", stream.bitrate)
        print("Downloading...")
        file_config = dict(
            output_path=tempfile.gettempdir(),
            filename='yt-only-audio.mp4'
        )
        self.mp4path = stream.get_file_path(**file_config)
        pgb = ProgressBar(maxval=stream.filesize).start()

        stream.download(**file_config, skip_existing=False)
        pgb.finish()

    def download_thumbnail(self):
        from urllib.request import urlopen
        import mimetypes

        self.thumbnailMimeType = mimetypes.guess_type(self.youtube.thumbnail_url)[0]
        self.thumbnailData = urlopen(self.youtube.thumbnail_url).read()

    def convertFileFormat(self):
        from moviepy.editor import AudioFileClip

        AudioFileClip(self.mp4path).write_audiofile(self.mp3path)

    def manipulateMetadata(self):
        import eyed3.mp3
        from eyed3.id3.frames import ImageFrame

        audiofile: eyed3.core.AudioFile = eyed3.load(self.mp3path)
        if audiofile.tag is None:
            audiofile.initTag()
        tag: eyed3.mp3.id3.Tag = audiofile.tag

        tag.title = self.title
        tag.artist = self.creator

        tag.images.set(
            ImageFrame.FRONT_COVER,
            self.thumbnailData,
            self.thumbnailMimeType
        )

        # tag.lyrics.set("")

        tag.save()


def fix_filename(filename: str) -> str:
    import re
    return re.sub(r'[^\w\-_. ()]', '_', filename)
