#!/usr/bin/python3
r"""
download the mp3 part of a YouTube-Video

tags: eyed3.core.Tag = eyed3.load(...).tag
tag.title =
tag.artist =
tag.save()

from pytube import YouTube as YouTubeVideo
from moviepy.editor import AudioFileClip
"""
import tempfile
import sys
import os.path as path

import pytube.exceptions
from pytube import YouTube


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
    youtube: YouTube
    creator: str
    title: str

    def __init__(self, url: str):
        self.url = url

    def execute(self):
        self.findAndValidate()
        self.collectMetadata()
        self.downloadAudio()
        self.convertFileFormat()
        self.manipulateMetadata()

    def findAndValidate(self):
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

        self.mp3path = path.abspath(fix_filename(title) + '.mp3')

        left, sep, right = title.partition('-')
        if not sep:  # - is not the seperator
            print("Couldn't autodetect right title")
            sep = input(f"Please enter the Seperator for '{title}' (Return of it's the title): ")
            if not sep:
                self.title = title
                self.creator = author
                return
            else:
                left, sep, right = title.partition(sep)
                if not sep:  # still failed
                    raise NameError("failed to autodetect title")

        left = left.strip()
        right = right.strip()

        a = int(input(f"please select title '{left}'(1) '{right}'(2) "))

        if a == 1:
            self.title = left
            self.creator = right
        elif a == 2:
            self.title = right
            self.creator = left
        else:
            raise ValueError()

    def downloadAudio(self):
        print("Searching for download")
        try:
            stream = self.youtube.streams.get_audio_only()
        except pytube.exceptions.PytubeError:
            raise RuntimeError("Failed to find audio-download")
        print("Download with quality of", stream.bitrate, "...")
        file_config = dict(
            output_path=tempfile.gettempdir(),
            filename='yt-only-audio.mp4'
        )
        self.mp4path = stream.get_file_path(**file_config)
        stream.download(**file_config, skip_existing=False)

    def convertFileFormat(self):
        from moviepy.editor import AudioFileClip

        AudioFileClip(self.mp4path).write_audiofile(self.mp3path)

    def manipulateMetadata(self):
        import eyed3.mp3

        file: eyed3.core.AudioFile = eyed3.load(self.mp3path)
        tag: eyed3.mp3.id3.Tag = file.tag
        tag.title = self.title
        tag.artist = self.creator
        tag.save()


def fix_filename(filename: str) -> str:
    import re
    return re.sub(r'[^\w\-_. ()]', '_', filename)
