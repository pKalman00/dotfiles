vim.g.mapleader = " "

vim.keymap.set('n', '<leader>pv', ':NvimTreeToggle<CR>')

vim.keymap.set({ "n", "v" }, "<leader>pf", function()
    require("conform").format({ bufnr = vim.api.nvim_get_current_buf() })
end, { desc = "Format current buffer (Conform)" })

vim.keymap.set('n', '<leader>pc', ':CsvViewToggle<CR>')

vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, { desc = "Rename symbol" })
