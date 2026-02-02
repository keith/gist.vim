" Gist.vim - Submit gists from Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.2.0

if exists('g:loaded_gist') && g:loaded_gist
  finish
endif
let g:loaded_gist = 1

function! s:ParseArgs(args)
  let l:opts = {
        \ 'public': get(g:, 'gist_default_private', 0) ? 0 : 1,
        \ 'open': get(g:, 'gist_open_url', 1),
        \ 'yank': get(g:, 'gist_copy_url', 0),
        \ 'description': ''
        \ }
  let l:desc_parts = []

  for l:arg in a:args
    if l:arg ==# '-p' || l:arg ==# '--private'
      let l:opts.public = 0
    elseif l:arg ==# '-P' || l:arg ==# '--public'
      let l:opts.public = 1
    elseif l:arg ==# '-o' || l:arg ==# '--open'
      let l:opts.open = 1
    elseif l:arg ==# '-y' || l:arg ==# '--yank'
      let l:opts.yank = 1
    else
      call add(l:desc_parts, l:arg)
    endif
  endfor

  let l:opts.description = join(l:desc_parts, ' ')
  return l:opts
endfunction

function! s:Gist(line1, line2, ...) abort
  let l:opts = s:ParseArgs(a:000)

  " Get description
  let l:description = l:opts.description
  if l:description ==# ''
    call inputsave()
    let l:description = input('Description: ')
    call inputrestore()
    redraw!
  endif

  if l:description ==# ''
    echohl ErrorMsg | echo 'You must enter a description' | echohl None
    return
  endif

  " Get filename
  let l:filename = expand('%:t')
  if l:filename ==# ''
    let l:filename = 'gist.txt'
  endif

  " Get content from buffer
  let l:lines = getline(a:line1, a:line2)
  let l:content = join(l:lines, "\n")

  " Create temp file
  let l:tempdir = tempname()
  call mkdir(l:tempdir, 'p')
  let l:tempfile = l:tempdir . '/' . l:filename
  call writefile(split(l:content, "\n", 1), l:tempfile)

  " Build gh command
  let l:cmd = ['gh', 'gist', 'create']
  if l:opts.public
    call add(l:cmd, '--public')
  endif
  if l:opts.open
    call add(l:cmd, '--web')
  endif
  call extend(l:cmd, ['--desc', l:description])
  call add(l:cmd, l:tempfile)

  " Run gh command
  let l:result = systemlist(join(map(l:cmd, 'shellescape(v:val)'), ' '))
  let l:exit_code = v:shell_error

  " Clean up temp file
  call delete(l:tempfile)
  call delete(l:tempdir, 'd')

  if l:exit_code != 0
    let l:error = join(l:result, "\n")
    if l:error =~# 'gh auth login'
      echohl ErrorMsg | echo "Not authenticated. Run 'gh auth login' first." | echohl None
    else
      echohl ErrorMsg | echo 'Error creating gist: ' . l:error | echohl None
    endif
    return
  endif

  let l:url = split(get(l:result, -1, ''), ' ')[-1]
  if match(l:url, '^https://') != 0
    echohl ErrorMsg | echo 'Failed to get gist URL from gh output: ' . join(l:result, ' ') | echohl None
    return
  endif

  " Display URL
  echom l:url

  " Copy to clipboard if requested
  if l:opts.yank
    let @+ = a:url
  endif
endfunction

function! s:CompleteArguments(ArgLead, CmdLine, CursorPos)
  return ['--public', '--private', '--open', '--yank']
endfunction

command! -nargs=* -range=% -complete=customlist,s:CompleteArguments
      \ Gist call s:Gist(<line1>, <line2>, <f-args>)
