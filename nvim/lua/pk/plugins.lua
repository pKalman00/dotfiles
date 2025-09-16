return {
    'folke/lazy.nvim',

    {
        'nvim-telescope/telescope.nvim',
        tag = '0.1.8', -- Or branch = '0.1.x' if you prefer
        dependencies = { {'nvim-lua/plenary.nvim'} },
        config = function()
            -- This is the content from your after/plugin/telescope.lua
            local builtin = require('telescope.builtin')
            vim.keymap.set('n', '<leader>pf', builtin.find_files, { desc = "Telescope Find Files" })
            vim.keymap.set('n', '<C-p>', builtin.git_files, { desc = "Telescope Git Files" })
            vim.keymap.set('n', '<leader>ps', function()
                builtin.grep_string({ search = vim.fn.input("Grep > ") })
            end, { desc = "Telescope Grep String" }) -- Removed the trailing comma here
            -- Any other Telescope setup (e.g., custom pickers, themes) would go here
        end,
    }, -- This comma is correct as it separates the Telescope plugin table from the Nightfox plugin table

    {
        "EdenEast/nightfox.nvim",
        name = "nightfox", -- Lazy.nvim often prefers 'name' over 'as' for clarity
        lazy = false,      -- Load this plugin immediately
        priority = 1000,   -- Ensure theme loads before other things
        config = function()
            vim.cmd("colorscheme nightfox")
            -- If you want a specific style of nightfox (e.g., 'nightfox' or 'carbonfox'):
            -- require('nightfox').setup({ options = { style = "nightfox" } })
        end,
    },

    -- nvim-treesitter
    {
        'nvim-treesitter/nvim-treesitter',
        build = ":TSUpdate", -- This will run TSUpdate after installation/update
        config = function()
            -- This is the content from your after/plugin/treesitter.lua
            require'nvim-treesitter.configs'.setup {
                ensure_installed = { "c", "lua", "vim", "vimdoc", "query", "markdown", "markdown_inline" },
                sync_install = false,
                auto_install = true,
                highlight = {
                    enable = true,
                    additional_vim_regex_highlighting = false,
                },
                -- If you had an `indent` table, add it here:
                indent = { enable = true }, -- Assuming you want indent as well
            }
        end,
    },
}
