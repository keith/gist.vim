# Gist.vim

Gist.vim, as expected, is a plugin for creating gists straight from Vim.
It is also [well
documented](https://github.com/keith/gist.vim/blob/master/doc/gist.txt).


**Note:** Gist.vim requires Vim to be compiled with `+python`.


## Usage

This plugin adds two commands:

```
:Gist [-pPao] [DESCRIPTION]
:GistOpenLast
```

The Gist command creates a gist from the buffer you're currently
viewing. It uses the current filename and all of the content. If you
would just like to post a portion of the content, invoke the
`:'<,'>Gist` command with a visual selection.


Here are the flags you can use when calling `:Gist`. Any other trailing
text will be used for the description. If you don't provide any other
text you will be prompted for a description.

```
-P, --public: This creates a public Gist. This is the default.
            Set g:gist_default_private to change this default.

-p, --private: This creates a private gist. Public is the default.
              See g:gist_default_private to change this default.

-o, --open: Open the created Gist in the browser after it's created.
          This is on by default.
          See g:gist_open_url to change this default.
```

Credentials are pulled from your `~/.netrc` file. They need to be in
this format: (The URL can vary based on your `g:gist_base_url`)

```
machine api.github.com
  login <Username>
  password <Password>
```

If you're using two factor auth, provide a personal access token from
[here](https://github.com/settings/applications) as the password.


By default the gist is opened in the browser upon creation. You can
change this default by setting `g:gist_open_url` to 0.

If you don't have a preferred installation method check out
[vim-plug](https://github.com/junegunn/vim-plug)
