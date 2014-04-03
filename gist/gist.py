"""
Create gists straight from Vim
Maintained by: Keith Smiley <http://keith.so>
"""
from gist.auth import user
import argparse
import base64
import json
import os
import os.path
import urllib2
import vim
import subprocess
import sys


def main(args):
    name, unknown = parser.parse_known_args(args.split())
    data = data_for_args(name, unknown)

    u = None
    if not name.anonymous:
        u = user.User.from_netrc(url=github_url(), path=netrc_path())
        if not u:
            print("No user in %s with machine %s" %
                  (netrc_path(True), github_url()))
            return
    request = request_for_user(u)

    try:
        pipe = urllib2.urlopen(request, json.dumps(data))
    except urllib2.HTTPError, e:
        print(str(e.reason))
        return

    response = pipe.read()
    pipe.close()
    try:
        j = json.loads(response)
    except ValueError:
        print("Failed to decode the response to JSON")
    else:
        open_url(j["html_url"])


def netrc_path(default=False):
    """
    Return the settings based netrc path
    """
    path = vim.vars.get("gist_netrc_path", None)
    if not path and default:
        path = os.path.join(os.path.expanduser("~"), ".netrc")

    return path


def data_for_args(name, unknown):
    """
    Returns the hash for the given arguments
    """
    data = {'public': name.public}
    data['files'] = get_files(name)
    desc = ' '.join(unknown)
    if not desc:
        desc = get_description()
    data['description'] = desc
    return data


def auth_for_user(u):
    """
    Formats the base64 string based on a user
    """
    return base64.standard_b64encode("%s:%s" % (u.username, u.password))


def request_for_user(u):
    """
    Creates the URL request with the credentials
    """
    request = urllib2.Request(github_url("gists"))
    if u:
        auth = auth_for_user(u)
        request.add_header("Authorization", "Basic %s" % auth)
    return request


def github_url(path=""):
    """
    Get the Github API URL
    """
    url = vim.vars.get("gist_base_url", "https://api.github.com/")
    return os.path.join(url, path)


def open_url(url):
    """
    Open the URL in the browser
    """
    vim.command("redraw!")
    print(url)
    switch = vim.vars.get("gist_should_open_url", 1) == 1
    if switch:
        subprocess.call(["open", url])


def executable():
    """
    Get the executable used to open the URL
    """
    system = sys.platform
    prg = None
    if system.startswith('darwin'):
        prg = vim.vars.get("gist_executable_for_darwin", "open")
    elif system.startswith('linux'):
        prg = vim.vars.get("gist_executable_for_linux", None)
    elif system.startswith('win'):
        prg = vim.vars.get("gist_executable_for_windows", "explorer")

    return prg


def get_description():
    """
    Ask the user for a description of the gist
    """
    vim.eval("inputsave()")
    desc = vim.eval("inputdialog('Description: ')")
    vim.eval("inputrestore()")
    vim.command("redraw!")
    return desc


def get_files(args):
    """
    Get the text from the files specified by the arguments
    If there is a visual selection just that text is used
    Otherwise if all is passed all buffers are used
    """
    files = {}
    b = vim.current.buffer
    if args.count >= 0:
        files[buffer_filename(b)] = text_from_buffer(b, args.line1, args.line2)
        return files

    bufs = [b]
    if args.all:
        bufs = []
        for tab in vim.tabpages:
            for win in tab.windows:
                b = win.buffer
                if not is_directory(b):
                    bufs.append(b)

    for b in bufs:
        files[buffer_filename(b)] = text_from_buffer(b, 0, len(b))

    return files


def text_from_buffer(b, l1, l2):
    """
    Return the text from the given buffer between the given lines
    This starts at a line before the given index to get all the text
    From the array of lines, joined by a newline
    """
    if l1 > 0:
        l1 -= 1
    return {'content': '\n'.join(b[l1:l2])}


def buffer_filename(b):
    """
    Return just the filename of the given buffer
    """
    return os.path.basename(b.name)


def is_directory(b):
    """
    Return if the given buffer is a directory
    """
    return os.path.isdir(b.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type=int)
    parser.add_argument('--line1', type=int, metavar='start')
    parser.add_argument('--line2', type=int, metavar='end')
    private_default = vim.vars.get("gist_default_private", 0) == 1
    parser.add_argument('-P', '--public', action='store_true',
                        dest='public', default=(not private_default))
    parser.add_argument('-p', '--private', action='store_false',
                        dest='public')
    parser.add_argument('-a', '--all', action='store_true',
                        default=False)
    parser.add_argument('-A', '--anonymous', action='store_true',
                        default=False)
