return {
    "stevearc/conform.nvim",
    event = { "BufReadPre", "BufNewFile" },
    opts = {
        formatters_by_ft = {
            lua = { "stylua" },
            python = { "autopep8" },
            rust = { "rustfmt" },
            c = { "clang_format" },
            cpp = { "clang_format" },
            java = { "clang_format" },
            json = { "jq" },
            markdown = { "prettier", "cbfmt" },
            html = { "prettier" },
            css = { "prettier" },
            javascript = { "prettier" },
        },
        --		format_on_save = {
        --			timeout_ms = 500,
        --			lsp_format = "fallback",
        --		},
    },
}
