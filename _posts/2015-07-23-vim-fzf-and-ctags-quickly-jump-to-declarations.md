---
layout: post
title: Vim, FZF and Ctags - quickly jump to declarations
tags: "fzf, ctags, vim"
category: en
published: true
---

I decided to refuse CtrlP in favor of FZF. FZF is more universal tool which can work outside the editor. I propose the solution, on the basis of FZF and ctags which allows to quickly pass on methods, imports, classes, etc. (thanks for [@junegunn](https://github.com/junegunn)). This solution has an advantage, it doesn't create the tags file and works only within the current buffer:

{% gist f24c36c18b7f64e16b4f btags.vim %}

Here is how it looks in work:


![Vim and ctags with FZF quickly jump to declarations](/assets/article_images/2015-07-23-vim-fzf-and-ctags-quickly-jump-to-declarations/vim-ctags-fzf.png "Vim and ctags with FZF quickly jump to declarations")
