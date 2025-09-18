return {
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