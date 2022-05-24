# <img width=auto height="30" src="https://raw.githubusercontent.com/PlayerG9/yt-command/master/README.assets/repo-icon.png" alt="" /> yt-command
command tool to search for YouTube videos and to download them

```text
        _                                                      _ 
  _   _| |_       ___ ___  _ __ ___  _ __ ___   __ _ _ __   __| |
 | | | | __|____ / __/ _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` |
 | |_| | ||_____| (_| (_) | | | | | | | | | | | (_| | | | | (_| |
  \__, |\__|     \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|
  |___/                                                          
```

# how to install
```commandline
$ cd path/to/directory/you/like
$ git clone https://github.com/PlayerG9/yt-command.git
$ yt-command/install.sh
```
run `yt --version` to test if the installation was successful

## what does the installation do?
- create a python-virtual-environment and install required packages
  - dir: `/path/to/yt-command/.venv/*`
- create an alias
  - line: `alias yt="/path/to/yt-command/sry/yt/run.sh` to `~/.bash_aliases`
- add bash-completion
  - file: `~/bash_completion.d/yt-completion.bash`
  - line: `source "~/bash_completion.d/yt-completion.bash"` to `~/.bashrc`
