import os
import pynvim
import libtmux
import re

@pynvim.plugin
class Nvimux(object):
    def __init__(self, nvim: pynvim.Nvim):
        self.nvim = nvim
        self.tmux_server: libtmux.Server
        self.tmux_session: libtmux.Session
        self.tmux_window: libtmux.Window
        self.tmux_pane: libtmux.Pane
        self.tmux_is_last_pane = 0
        self.transtab = str.maketrans("phjkl", "lLDUR")
        self.linked_pane: libtmux.Pane
        self._has_tmux = False
        self._is_linked = False
        if "TMUX" in os.environ:
            self._has_tmux = True
            self.tmux_server = libtmux.Server()
            tmux_session_id = os.getenv('TMUX').split(',')[2]
            self.tmux_session = self.tmux_server.get_by_id('${}'.format(tmux_session_id))
            self.tmux_window = self.tmux_session.attached_window
            self.tmux_pane = self.tmux_window.attached_pane
            self.linked_pane = None

    def _nvim_navigate(self, direction):
        return self.nvim.command("wincmd {}".format(direction))

    def _execute_tmux_cmd(self, cmd, args):
        return self.tmux_server.cmd("{} {}".format(cmd, args))

    def _tmux_select_pane(self, pane):
        return self.tmux_window.select_pane(pane)

    def _out_writre(self, mess):
        self.nvim.out_write("{}\n".format(mess))

    def _err_write(self, err):
        self.nvim.err_write("{}\n".format(err))

    def _no_tmux(self):
        self._err_write("No tmux server found. Please relaunch nvim inside a tmux session.")


    @pynvim.autocmd('WinEnter')
    def nvimux_win_enter_handle(self):
        self.tmux_is_last_pane = False

    @pynvim.function('NvimuxNavigate')
    def nvimux_navigate(self, args):
        if self._has_tmux:
            direction = args[0]
            nb = self.nvim.eval('winnr()')
            if not self.tmux_is_last_pane:
                self._nvim_navigate(direction)
            at_tab_page_end = (nb == self.nvim.eval('winnr()'))
            if at_tab_page_end:
                sel = "-{}".format(direction.translate(self.transtab))
                self._tmux_select_pane(sel)
        else:
            self._nvim_navigate(args[0])

    @pynvim.command('NvimuxLinkPane', nargs='*')
    def nvimux_link_pane(self, args):
        if self._has_tmux:
            if len(args) > 0:
                pane_to_link = self.tmux_window.get_by_id(args[0])
                if pane_to_link is None:
                    self._err_write("The specified pane was not found in your current window")
                    self._is_linked = False
                else:
                    self.linked_pane = pane_to_link
                    self._is_linked = True
            else:
                self._err_write("Please specify a pane to attach to")
                self._is_linked = False
        else:
            self._no_tmux()

    @pynvim.command('NvimuxOpenPane', nargs='*')
    def nvimux_open_pane(self, args):
        if self.tmux_server is not None:
            my_args = {
                'attach': False,
                'target': self.tmux_pane.get('pane_id'),
                'vertical': True,
                'start_dir': None
                }
            if '-a' in args:
                my_args['attach'] = True
            if '-t' in args:
                idx = args.index('-t')
                pane_regex = re.compile(r'^\%\d+$')
                try:
                    pane_num = pane_regex.search(args[idx+1])
                    if pane_num is None:
                        self._err_write("You must specify a valid pane after -t.")
                        return None
                    else:
                        target = pane_num.group()
                        my_args['target'] = target
                except IndexError as e:
                    self._err_write("Please specify a target after -t.")
                    return None
            if '-h' in args:
                my_args['vertical'] = False
            if '-d' in args:
                idx = args.index('-d')
                my_dir = None
                try:
                    my_dir = args[idx + 1]
                    my_args['start_dir'] = my_dir
                    arg_regex = re.compile(r'\-[a-z]')
                    arg = arg_regex.search(my_dir)
                    if arg is None:
                        my_dir = os.path.expanduser(my_dir)
                        my_dir = os.path.expandvars(my_dir)
                        if os.path.isdir(my_dir):
                            my_args['start_dir'] = my_dir
                        else:
                            self._err_write("Please specify a valid directory after -d.")
                            return None
                    else:
                        self._err_write("Please sepcify a valid directory after -d.")
                        return None
                except IndexError as e:
                    self._err_write('Please specify a path after -d')
                    return None
            return self.tmux_window.split_window(
                attach=my_args['attach'],
                start_directory=my_args['start_dir'],
                target=my_args['target'],
                vertical=my_args['vertical'])
        else:
            self._no_tmux()
            return None

    @pynvim.command('NvimuxOpenAndLink', nargs='*')
    def nvimux_open_and_link(self, args):
        pane = self.nvimux_open_pane(args)
        if isinstance(pane, libtmux.Pane):
            self.nvimux_link_pane([pane.get('pane_id')])
        else:
            self._err_write('Failed to open a pane, please try again.')

    @pynvim.command('NvimuxSendCommand', nargs='*')
    def nvimux_send_command(self, args):
        if self._has_tmux:
            if self._is_linked:
                if len(args) < 1:
                    self._err_write("Please specify a command to send.")
                else:
                    cmd_str = args[0]
                    args_str = None
                    if len(args) > 1:
                        args_str = " ".join(args[1:])
                    cmd = self.linked_pane.cmd(cmd_str, args_str)
                    if cmd.stderr:
                        self._err_write("Command: {} returned error: {}".format(cmd.cmd, cmd.stderr))
                    else:
                        self._out_writre("Command: {} return {}".format(cmd.cmd, cmd.stdout))
            else:
                self._err_write("Please link a pane before sending a command to tmux.")
        else:
            self._no_tmux()

    @pynvim.command('NvimuxSendKeys', nargs="*")
    def nvimux_send_keys(self, args):
        if self._has_tmux:
            if self._is_linked:
                my_args = {
                        'enter': True,
                        'suppress_history': True,
                        'literal': True
                        }
                if '-e' in args:
                    my_args['enter'] = False
                    args = [x for x in args if x != '-e']
                if '-l' in args:
                    my_args['literal'] = False
                    args = [x for x in args if x != '-l']
                if len(args) == 0:
                    self._err_write("Please specify keys to send")
                args = [x.replace(' ', '') for x in args]
                keys = " ".join(args)
                self.linked_pane.send_keys(keys, enter=my_args['enter'], literal=my_args['literal'], suppress_history = False)
            else:
                self._err_write("Please link a pane before sending keys")
        else:
            self._no_tmux()
