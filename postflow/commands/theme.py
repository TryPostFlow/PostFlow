# -*- coding: utf-8 -*-

import os
import sys
import zipfile
import shutil
import requests
import click
from flask import current_app

from postflow.commands.base import postflow


@postflow.group()
def theme():
    """Create, update or delete theme."""
    pass


def download_theme(path):
    theme_name = path.split('/')[-1]
    themes_folder = os.path.join(current_app.instance_path, 'content/themes')
    theme_path = os.path.join(themes_folder, theme_name)

    if os.path.exists(theme_path):
        if click.confirm(
                click.style(
                    "Existing theme found. Do you want to override it?",
                    fg="magenta")):
            shutil.rmtree(theme_path)
        else:
            return theme_name

    file_path = os.path.join(themes_folder, "{}.zip".format(theme_name))
    link = "https://github.com/{}/archive/master.zip".format(path)

    with open(file_path, "wb") as f:
        sys.stdout.write("[+] Downloading {}\n".format(theme_name))
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()
            sys.stdout.write("\n")

    zip_ref = zipfile.ZipFile(file_path, 'r')
    repo_dir = zip_ref.namelist()[0]
    zip_ref.extractall(os.path.join(themes_folder))
    zip_ref.close()
    os.rename(
        os.path.join(themes_folder, repo_dir),
        os.path.join(themes_folder, theme_name))
    os.remove(file_path)
    sys.stdout.write(
        "[+] {} has been successfully downloaded!\n".format(theme_name))
    return theme_name


@theme.command("download")
@click.option("--path", "-u", help="The github path of the theme.")
def download(path):
    if not path:
        path = click.prompt(
            click.style(
                "Theme name (Github: user_name/repo_name)", fg="magenta"),
            type=str,
            default="TryPostFlow/Casper")
    download_theme(path)
