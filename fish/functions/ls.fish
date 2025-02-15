function ls --wraps=eza --description 'alias ls=eza'
  eza -a --group-directories-first $argv
        
end
