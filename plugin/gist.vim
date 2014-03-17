" Gist.vim - Submit gists from Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.0

if exists('g:loaded_gist') && g:loaded_gist
  finish
endif
let g:loaded_gist = 1

" Pass the arguments from the Vim CLI to python
function s:Gist(count, line1, line2, ...)
  let args = a:000 + ["--count", a:count] +
        \ ["--line1", a:line1] + ["--line2", a:line2]
  let file = expand('<sfile>:p:h') . '/python/gist.py'
  execute 'pyfile ' . file
  execute 'python main("' . join(args, " ") . '")'
endfunction

command! -nargs=? -range=% Gist call s:Gist(<count>, <line1>, <line2>, <f-args>)
