return {
    'folke/lazy.nvim',

    { "nvim-tree/nvim-web-devicons", opts = {} },
    
    {
        'nvim-telescope/telescope-fzf-native.nvim',
        build = 'cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release'
    },
    
    {
        "lewis6991/gitsigns.nvim",
        lazy = false, -- Load gitsigns on startup
        config = function()
            require("gitsigns").setup({})
        end,
    },
    
    {
        "vhyrro/luarocks.nvim",
        priority = 1000,
        config = true,
    },

    {
        'nvim-telescope/telescope.nvim',
        branch = '0.1.x',
        dependencies = { {'nvim-lua/plenary.nvim'} },
        config = function()
            local builtin = require('telescope.builtin')
            vim.keymap.set('n', '<leader>pf', builtin.find_files, { desc = "Telescope Find Files" })
            vim.keymap.set('n', '<C-p>', builtin.git_files, { desc = "Telescope Git Files" })
            vim.keymap.set('n', '<leader>ps', function()
                builtin.grep_string({ search = vim.fn.input("Grep > ") })
            end, { desc = "Telescope Grep String" }) -- Removed the trailing comma here
        end,
    },

    {
        "EdenEast/nightfox.nvim",
        name = "nightfox",
        lazy = false,
        priority = 999,
        config = function()
            vim.cmd("colorscheme nightfox")
        end,
    },

    {
        'nvim-treesitter/nvim-treesitter',
        build = ":TSUpdate",
        config = function()
            require'nvim-treesitter.configs'.setup {
                ensure_installed = { "c", "lua", "vim", "vimdoc", "query", "markdown", "markdown_inline" },
                sync_install = false,
                auto_install = true,
                highlight = {
                    enable = true,
                    additional_vim_regex_highlighting = false,
                },
                indent = { enable = true },
            }
        end,
    },
    {
        "nvim-tree/nvim-tree.lua",
        version = "*",
        lazy = false,
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },
        config = function()
            require("nvim-tree").setup {
                view = {
                    width = 30,
                    side = "right",
                    float = { enable = false, },
                },
                actions = {
                    open_file = { quit_on_open = true, },
                },
                git = { enable = true, },
                filters = { dotfiles = false, },
                update_focused_file = {
                    enable = true,
                    update_root = true,
                },
            }
        end,
    },
}
