" Gist.vim - Submit gists from Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.0

if exists('g:loaded_gist') && g:loaded_gist
  finish
endif
let g:loaded_gist = 1
let s:plug = expand("<sfile>:p:h:h")

function! s:LoadPythonScript()
  if exists('s:loaded_gist_python') && s:loaded_gist_python
    return
  endif
  let s:loaded_gist_python = 1

  let script = s:plug . '/gist/gist.py'
  execute 'python import sys'
  execute 'python sys.path.append("' . s:plug . '")'
  execute 'pyfile ' . script
endfunction

" Pass the arguments from the Vim CLI to python
function! s:Gist(count, line1, line2, ...)
  let args = a:000 + ["--count", a:count] +
        \ ["--line1", a:line1] + ["--line2", a:line2]
  try
    call s:LoadPythonScript()
    execute 'python main("' . join(args, " ") . '")'
  catch /^Vim\%((\a\+)\)\=:E880/
  endtry
endfunction

function! s:GistOpenLast()
  try
    call s:LoadPythonScript()
    execute 'python open_last_url()'
  catch /^Vim\%((\a\+)\)\=:E880/
  endtry
endfunction

command! -nargs=? -range=% Gist call s:Gist(<count>, <line1>, <line2>, <f-args>)
command!                   GistOpenLast call s:GistOpenLast()
