function gl --wraps='git log --oneline --graph --all --decorate' --description 'alias gl=git log --oneline --graph --all --decorate'
    git log --oneline --graph --all --decorate $argv
end
