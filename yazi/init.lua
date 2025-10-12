-- Full-border plugin
require("full-border"):setup {
    type = ui.Border.ROUNDED,
}

-- Git status plugin
require("git"):setup()

-- Symlink target in status bar
Status:children_add(function(self)
	local h = self._current.hovered
	if h and h.link_to then
		return " -> " .. tostring(h.link_to)
	else
		return ""
	end
end, 3300, Status.LEFT)

-- Recycle-bin plugin
require("recycle-bin"):setup()

-- Starship plugin
require("starship"):setup({
    hide_flags = false,
    flags_after_prompt = true,
    config_file = "~/.config/yazi/starship.toml",
})

-- oh-my-posh plugin
-- require("omp"):setup({ config = "~/.config/yazi/omp.json" })
