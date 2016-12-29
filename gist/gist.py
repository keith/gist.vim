"""
Create gists straight from Vim
Maintained by: Keith Smiley <http://keith.so>
"""

from gist.auth.user import User
import argparse
import base64
import distutils.spawn
import json
import os
import os.path
import subprocess
import sys
import urllib2
import vim


def main(args):
    name, unknown = parser.parse_known_args(args.split())
    data = data_for_args(name, unknown)
    if not data:
        return

    user = None
    if not name.anonymous:
        user = User.from_netrc(url=github_url())
        if not user:
            print("No user with machine %s" % github_url())
            return
    request = request_for_user(user)

    try:
        pipe = urllib2.urlopen(request, json.dumps(data))
    except urllib2.HTTPError as e:
        if e.getcode():
            print("Got 404, update your token to with the gist scope")
        else:
            print(str(e.reason))
        return
    except urllib2.URLError as e:
        print(e.reason)
        return

    response = pipe.read()
    pipe.close()
    try:
        j = json.loads(response)
    except(ValueError):
        print("Failed to decode the response to JSON")
    else:
        url = j["html_url"]
        open_url(url, browser=name.open_browser)
        save_url(url)



def data_for_args(name, unknown):
    """
    Returns the hash for the given arguments
    """
    data = {'public': name.public}
    data['files'] = get_files(name)
    desc = ' '.join(unknown)
    if not desc:
        desc = get_description()
    if not desc:
        print("You must enter a description")
        return None
    data['description'] = desc
    return data


def auth_for_user(user):
    """
    Formats the base64 string based on a user
    """
    return base64.standard_b64encode("%s:%s" % (user.username, user.password))


def request_for_user(user):
    """
    Creates the URL request with the credentials
    """
    request = urllib2.Request(github_url("gists"))
    if user:
        auth = auth_for_user(user)
        request.add_header("Authorization", "Basic %s" % auth)
    return request


def github_url(path=""):
    """
    Get the Github API URL
    """
    url = vim.vars.get("gist_base_url", "https://api.github.com/")
    return os.path.join(url, path)


def save_url(url):
    """
    Set the last URL as a vim variable for later access
    """
    vim.vars["gist_last_gist_url"] = url


def open_last_url():
    """
    Get the last URL from vim and open it
    """
    url = vim.vars.get("gist_last_gist_url", "")
    open_url(url, browser=True)


def open_url(url, browser=False):
    """
    Open the URL in the browser
    """
    if not url:
        print("No stored Gist URL")
        return

    vim.command("redraw!")
    print(url)

    if not browser:
        return

    prg = executable()
    if not prg:
        print("No URL handler found see :help Gist for more info")
        return

    subprocess.call([prg, url])


def executable():
    """
    Get the executable used to open the URL
    """
    system = sys.platform
    prg = None
    if system.startswith('darwin'):
        prg = vim.vars.get('gist_executable_for_mac', 'open')
    elif system.startswith('linux'):
        prg = linux_executable()
    elif system.startswith('cygwin'):
        prg = vim.vars.get('gist_executable_for_cygwin', 'cygstart')
    elif system.startswith('win'):
        prg = vim.vars.get('gist_executable_for_windows', 'explorer')

    if not executable_exists(prg):
        return None

    return prg


def linux_executable():
    """
    Choose a linux executable if a known one exists
    """
    prg = vim.vars.get('gist_executable_for_linux', None)
    if prg:
        return prg

    prgs = ['xdg-open', 'gvfs-open', 'gnome-open']
    for t in prgs:
        if executable_exists(t):
            return t

    return prg


def executable_exists(prg):
    """
    Make sure an executable exists. If python 3 ever becomes
    the norm there is a better method for this
    """
    return distutils.spawn.find_executable(prg)


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
    # if args.all:
    #     bufs = []
    #     for tab in vim.tabpages:
    #         for win in tab.windows:
    #             b = win.buffer
    #             if not is_directory(b):
    #                 bufs.append(b)

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
    open_default = vim.vars.get("gist_open_url", 1) == 1
    parser.add_argument('-P', '--public', action='store_true',
                        dest='public', default=(not private_default))
    parser.add_argument('-p', '--private', action='store_false',
                        dest='public')
    parser.add_argument('-a', '--anonymous', action='store_true',
                        default=False)
    parser.add_argument('-o', '--open', action='store_true',
                        dest='open_browser', default=open_default)
