# Gist.vim

Gist.vim, as expected, is a plugin for creating gists straight from Vim.
It is also [well
documented](https://github.com/Keithbsmiley/gist.vim/blob/master/doc/gist.txt)

This plugin adds two commands:

```
:Gist [-pPao] [DESCRIPTION]
:GistOpenLast
```

Credentials are pulled from your `~/.netrc` file. You can change the default
location with `g:gist_netrc_path`. They need to be in this format:
(The URL can vary based on your `g:gist_base_url`)

```
machine <api.github.com>
  login <Username>
  password <Password>
```

By default the gist is opened in the browser upon creation. You can
change this default by setting `g:gist_open_url` to 0.

## Installation

### With [Vundle](https://github.com/gmarik/vundle)

Add:

```
Bundle 'Keithbsmiley/gist.vim'
```

To your `.vimrc` and run `BundleInstall` from within vim or `vim +BundleInstall +qall` from the command line

### With [Pathogen](https://github.com/tpope/vim-pathogen)

```
cd ~/.vim/bundle
git clone https://github.com/Keithbsmiley/gist.vim.git
```

To generate the helptags afterwards run `:Helptags`

## Development

If you find any bugs or want any features added please submit an
[issue](https://github.com/Keithbsmiley/gist.vim/issues/new).
