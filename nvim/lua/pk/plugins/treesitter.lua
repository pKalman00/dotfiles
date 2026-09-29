return {
  "nvim-treesitter/nvim-treesitter",
  lazy = false,
  build = ":TSUpdate",
  config = function()
    require("nvim-treesitter").install({
      "lua", "vim", "vimdoc", "query", "python", "c", "rust", "csv",
    })

    vim.api.nvim_create_autocmd("FileType", {
      callback = function(args)
        if vim.bo[args.buf].buftype ~= "" then
          return
        end

        local lang = vim.treesitter.language.get_lang(
          vim.bo[args.buf].filetype
        )
        if not lang then
          return
        end

        local ok, loaded = pcall(vim.treesitter.language.add, lang)
        if not ok or not loaded then
          return
        end

        vim.treesitter.start(args.buf, lang)
      end,
    })
  end,
}
