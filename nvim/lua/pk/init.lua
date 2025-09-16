vim.cmd("set rtp+=" .. vim.fn.stdpath("config") .. "/lua")
require("pk.set")

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable", -- latest stable release
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup("pk.plugins", {
    change_detection = {
        enabled = true,
        notify = false,
    },
})

require("pk.remap")

vim.cmd([[
    augroup LazyReload
        autocmd!
        autocmd BufWritePost lua/pk/*.lua source <afile> | Lazy sync
    augroup end
]])
