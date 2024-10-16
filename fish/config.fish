if status is-interactive
    # Commands to run in interactive sessions can go here
    # set
    set -g fish_greeting ''
    set JAVA_HOME /usr/java/jdk-17.0.1/
    # $PATH
    fish_add_path /home/linuxbrew/.linuxbrew/bin/
    fish_add_path /usr/java/jdk-17.0.1/bin/
    fish_add_path ~/.local/bin/
    fish_add_path ~/bin/
    fish_add_path ~/Documents/adb/platform-tools/
    fish_add_path ~/.cargo/bin/
    fish_add_path ~/Documents/cmdline-tools/latest/bin/
    fish_add_path ~/Documents/build-tools/34.0.0/
    fish_add_path /opt/nvim-linux64/bin/
    # sources
    oh-my-posh init fish --config ~/.config/oh-my-posh/omp.json | source
    zoxide init fish --cmd cd | source
end
