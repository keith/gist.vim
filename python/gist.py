import argparse
import vim


def github_url(path):
    # TODO: Based off variable for enterprise
    return "https://api.github.com/%s" % path


def main(args):
    name = parser.parse_args(args.split())
    parser.print_help()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type=int)
    parser.add_argument('--line1', type=int, metavar='start')
    parser.add_argument('--line2', type=int, metavar='end')
    private_default = vim.vars.get("gist_default_private", False) == 1
    parser.add_argument('-P', '--public', action='store_true',
                        dest='public', default=(not private_default))
    parser.add_argument('-p', '--private', action='store_true',
                        dest='private', default=private_default)
