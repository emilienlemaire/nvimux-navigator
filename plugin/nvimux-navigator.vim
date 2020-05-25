if !get(g:, 'nvimux_no_binding', 0)
    nnoremap <silent> <c-h> :call NvimuxNavigate('h')<cr>
    nnoremap <silent> <c-j> :call NvimuxNavigate('j')<cr>
    nnoremap <silent> <c-k> :call NvimuxNavigate('k')<cr>
    nnoremap <silent> <c-l> :call NvimuxNavigate('l')<cr>
endif
