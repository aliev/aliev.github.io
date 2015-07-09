---
layout: post
title: Vim, FZF и Ag
tags: "fzf, ag, vim"
category: ru
published: true
---

FZF это универсальный и очень быстрый инструмент Fuzzy Finder написанный на языке Go, который может работать как отдельная утилита.

Для начала необходимо установить FZF по [инструкции](https://github.com/junegunn/fzf/). Затем добавьте в vimrc строку set rtp+=~/.fzf

Скрипт для интеграции с Ag:

{% highlight vim %}
function! s:ag_to_qf(line)
  let parts = split(a:line, ':')
  return {'filename': parts[0], 'lnum': parts[1], 'col': parts[2],
        \ 'text': join(parts[3:], ':')}
endfunction

function! s:ag_handler(lines)
  if len(a:lines) < 2 | return | endif

  let cmd = get({'ctrl-x': 'split',
               \ 'ctrl-v': 'vertical split',
               \ 'ctrl-t': 'tabe'}, a:lines[0], 'e')
  let list = map(a:lines[1:], 's:ag_to_qf(v:val)')

  let first = list[0]
  execute cmd escape(first.filename, ' %#\')
  execute first.lnum
  execute 'normal!' first.col.'|zz'

  if len(list) > 1
    call setqflist(list)
    copen
    wincmd p
  endif
endfunction

command! -nargs=1 Ag call fzf#run({
\ 'source':  'ag --nogroup --column --color "'.escape(<q-args>, '"\').'"',
\ 'sink*':    function('<sid>ag_handler'),
\ 'options': '--ansi --expect=ctrl-t,ctrl-v,ctrl-x '.
\            '--multi --bind ctrl-a:select-all --color hl:68,hl+:110',
\ 'down':    '50%'
\ })
{% endhighlight %}

После перезагрузки редактора у нас появится команда :Ag которая принимает единственный аргумент - искомую строку. В случае, если искомая строка была найдена в нескольких файлах, их можно выбрать воспользовавшись клавишей tab.


