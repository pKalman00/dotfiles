return {
    {
        'nvim-telescope/telescope.nvim',
        branch = '0.1.x',
        dependencies = { {'nvim-lua/plenary.nvim'} },
        config = function()
            local builtin = require('telescope.builtin')
            vim.keymap.set('n', '<leader>pt', builtin.find_files, { desc = "Telescope Find Files" })
            vim.keymap.set('n', '<C-p>', builtin.git_files, { desc = "Telescope Git Files" })
            vim.keymap.set('n', '<leader>ps', function()
                builtin.grep_string({ search = vim.fn.input("Grep > ") })
            end, { desc = "Telescope Grep String" })
        end,
    },
}
