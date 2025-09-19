return {
    {
        "jay-babu/mason-nvim-dap.nvim",
        dependencies = {
            "williamboman/mason.nvim",
            "mfussenegger/nvim-dap",
        },
        config = function()
            require("mason-nvim-dap").setup({
                ensure_installed = {
                    "codelldb",
                    "debugpy",
                    "java-debug-adapter",
                    "bash-debug-adapter",
                    "js-debug-adapter",
                },
                automatic_installation = true,
                handlers = {
                    function(adapter_name)
                        require("mason-nvim-dap").default_setup(adapter_name)
                    end,
                }
            })
        end,
    },

    {
        "mfussenegger/nvim-dap",
        dependencies = {
            {
                "igorlfs/nvim-dap-view",
                opts = {
                    windows = {
                        terminal = {
                            position = "right",
                        },
                    },
                },
                keys = {
                    {
                        "<leader>dt",
                        "<cmd>DapViewToggle<cr>",
                        desc = "[T]oggle DAP View",
                    },
                },
            },
        },
        config = function()
            local dap = require("dap")
            local dv = require("dap-view")

            dap.listeners.before.attach["dap-view-config"] = function()
                dv.open()
            end
            dap.listeners.before.launch["dap-view-config"] = function()
                dv.open()
            end
            dap.listeners.before.event_terminated["dap-view-config"] = function()
                dv.close()
            end
            dap.listeners.before.event_exited["dap-view-config"] = function()
                dv.close()
            end

            dap.adapters.codelldb = {
                type = "executable",
                command = "codelldb",
            }

            dap.configurations.c = {
                {
                    name = "Launch file",
                    type = "codelldb",
                    request = "launch",
                    expressions = "native",
                    program = function()
                        return vim.fn.input("Path to executable: ", vim.fn.getcwd() .. "/", "file")
                    end,
                    cwd = "${workspaceFolder}",
                    stopOnEntry = false,
                },
            }

            dap.configurations.cpp = dap.configurations.c

            dap.configurations.python = {
                {
                    type = "python",
                    request = "launch",
                    name = "Launch file",
                    program = "${file}",
                    pythonPath = function()
                        local venv = os.getenv("VIRTUAL_ENV")
                        if venv then
                            return venv .. "/bin/python"
                        else
                            return vim.fn.exepath("python") or "python"
                        end
                    end,
                    cwd = "${workspaceFolder}",
                    stopOnEntry = false,
                },
            }

            -- Configure Keymaps
            vim.keymap.set("n", "<leader>db", "<cmd>DapToggleBreakpoint<cr>", { desc = "Toggle [B]reakpoint" })
            vim.keymap.set("n", "<leader>dc", "<cmd>DapContinue<cr>", { desc = "[D]AP [C]ontinue" })
            vim.keymap.set("n", "<leader>dn", "<cmd>DapNew<cr>", { desc = "[D]AP [N]ew" })
            vim.keymap.set("n", "<leader>dw", "<cmd>DapViewWatch<cr>", { desc = "[D]AP [W]atch" })
            vim.keymap.set("n", "<F9>", "<cmd>DapStepOver<cr>", { desc = "Step Over" })
            vim.keymap.set("n", "<F8>", "<cmd>DapStepInto<cr>", { desc = "Step Into" })
            vim.keymap.set("n", "<F7>", "<cmd>DapStepOut<cr>", { desc = "Step Out" })

            -- Configure custom icons
            vim.fn.sign_define("DapBreakpoint", { text = "󰧟", texthl = "LspDiagnosticsError" })
        end,
    },
}
