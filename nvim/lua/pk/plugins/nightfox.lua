return {
    {
        "EdenEast/nightfox.nvim",
        name = "nightfox",
        lazy = false,
        priority = 999,
        config = function()
            vim.cmd("colorscheme nightfox")
        end,
    },
}