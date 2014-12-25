import re
import subprocess

__author__ = 'cybran'

import requests
from lxml import html
from clint.textui import progress
from os.path import expanduser, join
from os import remove

import tarfile


def bytes_to_megabytes(bytes):
    return (bytes / 1024) / 1024


page = requests.post('http://www.jetbrains.com/pycharm/download/download_thanks.jsp',
                     {'os': 'linux', 'edition': 'prof'}
)
tree = html.fromstring(page.text)
download_link = tree.xpath("//a[text()='direct link']")[0].attrib['href']

print "Downloading from"
print download_link

with open('pycharm.tar.gz', 'wb') as archive:
    r = requests.get(download_link, stream=True)
    size = int(r.headers.get('content-length'))
    print "Archive size is", bytes_to_megabytes(size), "MB"

    if not r.ok:
        raise Exception("Something wrong with the link :(")

    for block in progress.bar(r.iter_content(chunk_size=1024), expected_size=(size / 1024) + 1):
        if block:
            archive.write(block)
print "Downloaded!"

print "Extracting the archive..."

install_path = join(expanduser("~"))

with tarfile.TarFile.open('pycharm.tar.gz', 'r') as archive:
    archive.extractall(install_path)

remove('pycharm.tar.gz')
print "Extracted to", install_path

unpacked_name = "pycharm-" + re.findall(r'([\d\.]+\d)', download_link)[0]

print "Executing PyCharm..."
subprocess.Popen(join(install_path, unpacked_name, "bin", "pycharm.sh"), shell=True)
