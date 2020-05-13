Nvimux-Navigator
=======================
This plugin enables you to navigate navigate seamlessly between nvim and tmux. It is greatly inspired by Chris Tommey's [vim-tmux-navigator](https://github.com/christoomey/vim-tmux-navigator).

Installation
--------------
### Requirements

Nvimux requires that you have Neovim with Python3 support and libtmux:

``` sh
pip install pynvim
pip install libtmux
```

### Installation

You can then install it like your others Nvim plugins and run `:UpdateRemotePlugins`. You should restart Nvim after that.

### Tmux

Please check Chris Tommey's [vim-tmux-navigator](https://github.com/christoomey/vim-tmux-navigator) and add his tmux snippet in your `.tmux.conf`

Usage
------------
### Functions

You can map the `NvimuxNavigate(arg)` function to your preferred keys, it works with or without tmux.
The arg can be `h`, `j`, `k`, or `l` respectively for left, down, up and right.


### Commands

Use these commands to manipulate your tmux panes directly from Nvim

Command | Action
--- | ---
`NvimuxLinkPane (pane_id)` | `pane_id`: Specify the pane you'd like to link Nvim with. Must be under the format: `%n`.
`NvimuxOpenPane` <br> `[-a\|-t target]` <br> `[-v\|-d dir]` | <ul> <li>`-a`: attach to the new opened pane</li> <li>`-t target`: specify the target from which to create the new pane</li> <li>`-v`: open the new pane vertically</li> <li>`-d dir`: open the pane in the `dir` directory</li></ul>
`NvimuxOpenAndLink` <br> `[-a\|-t target]` <br> `[-v\|-d dir]` | The arguments are the same as for `NvimuxOpenPane`, only it links the newly opened pane to Nvim.
`NvimuxSendCommand (cmd)` | Send the `cmd` command to the linked pane. If no pane is linked an error is returned.
`NvimuxSendKeys [-e\|-l] (keys)` | Send the `keys` to the tmux linked pane as they are written. If no pane is linked an error is returned. <br> <ul> <li>`-e`: The enter key will not be pressed after the keys</li> <li>`-l`: The keys will not be send literally</li> </ul>

Contributing
-------------
Please feel free to open an issue if you think of an improvement or find a bug. Any help is appreciated.
