" Gist.vim - Submit gists from Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.1

if exists('g:loaded_gist') && g:loaded_gist
  finish
endif
let g:loaded_gist = 1
let s:plug = expand('<sfile>:p:h:h')

" There are too many differences with python 3 for me to want and try
" to support it at this point
if !has('python') " && !has('python3')
  command! Gist :echohl ErrorMsg |
        \ echo 'Gist.vim requires Vim compiled with +python' |
        \ echohl None<CR>
  finish
endif

let s:python_version = 'python '
let s:pyfile_version = 'pyfile '
" if has('python3')
"   let s:python_version = 'python3 '
"   let s:pyfile_version = 'py3file '
" endif

function! s:LoadPythonScript()
  if exists('s:loaded_gist_python') && s:loaded_gist_python
    return
  endif
  let s:loaded_gist_python = 1

  let l:script = s:plug . '/gist/gist.py'
  execute s:python_version . 'import sys'
  execute s:python_version . 'sys.path.append("' . s:plug . '")'
  execute s:pyfile_version . l:script
endfunction

function! s:CompleteArguments(ArgLead, CmdLine, CursorPos)
  return [
        \ '--public',
        \ '--private',
        \ '--anonymous',
        \ '--open'
      \ ]
endfunction

" Pass the arguments from the Vim CLI to python
function! s:Gist(count, line1, line2, ...)
  let l:args = a:000 + ['--count', a:count] +
        \ ['--line1', a:line1] + ['--line2', a:line2]
  try
    call s:LoadPythonScript()
    execute s:python_version . ' main("' . join(l:args, ' ') . '")'
  catch /^Vim\%((\a\+)\)\=:E880/
  endtry
endfunction

function! s:GistOpenLast()
  try
    call s:LoadPythonScript()
    execute s:python_version . ' open_last_url()'
  catch /^Vim\%((\a\+)\)\=:E880/
  endtry
endfunction

command! -nargs=? -range=% -complete=customlist,s:CompleteArguments
      \ Gist call s:Gist(<count>, <line1>, <line2>, <f-args>)
command! GistOpenLast call s:GistOpenLast()
