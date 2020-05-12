Nvimux
=======================
This plugin enables you to navigate navigate seamlessly between nvim and tmux. It is greatly inspired by Chris Tommey's [vim_-tmux-navigator](https://github.com/christoomey/vim-tmux-navigator).

Installation
--------------
### Requirements

Nvimux requires that you have Neovim with Python3 support and libtmux:

``` sh
pip install pynvim
pip install libtmux
```

### Installation

You can then install it likae your other Nvim plugins and run `:PlugInstall`

Usage
------------
### Functions

You can map the `NvimuxNavigate(arg)` function to your prefered keys, it works with or without tmux.
The arg can be `h`, `j`, `k`, or `l` respectively for left, down, up and right.


### Commands

Command | Arguments | Action
--- | --- | ---
`NvimuxLinkPane` | pane__id | `pane_id`: Specify the pane you'd like to link Nvim with. Must be under the format: `%n`.
