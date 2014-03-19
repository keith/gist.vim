import argparse
import os.path
from gist.auth import user
import vim
import json


def github_url(path):
    # TODO: Based off variable for enterprise
    return "https://api.github.com/%s" % path


def main(args):
    name = parser.parse_args(args.split())
    # print name
    # parser.print_help()
    data = {'public': name.public}
    data['files'] = get_files(name)
    vim.eval("inputsave()")
    desc = vim.eval("inputdialog('Description: ')")
    vim.eval("inputrestore()")
    data['description'] = desc
    # print json.dumps(data)
    # TODO: request
    u = user.User.from_netrc(url="github.com")
    print u


def get_files(args):
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
    # TODO: Must join strings in array by newline
    if l1 > 0:
        l1 -= 1
    return b[l1:l2]


def buffer_filename(b):
    return os.path.basename(b.name)


def is_directory(b):
    return int(vim.eval("isdirectory(expand('%s'))" % b.name)) == 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type=int)
    parser.add_argument('--line1', type=int, metavar='start')
    parser.add_argument('--line2', type=int, metavar='end')
    private_default = vim.vars.get("gist_default_private", False) == 1
    parser.add_argument('-P', '--public', action='store_true',
                        dest='public', default=(not private_default))
    parser.add_argument('-p', '--private', action='store_false',
                        dest='public')
    parser.add_argument('-a', '--all', action='store_true',
                        default=False)
