-- Build-in screen
hl.monitor({
    output              = "eDP-1",
    mode                = "2880x1800@120.00Hz",
    -- mode                = "2880x1800@60.00Hz",
    position            = "0x0",
    scale               = "2.00",
    -- bitdepth            = 10,
    -- cm                  = "wide",
    supports_wide_color = 1,
    supports_hdr        = 1,
    sdr_min_luminance   = 0.005,
    sdr_max_luminance   = 200,
    min_luminance       = 0,
    max_luminance       = 617,
    max_avg_luminance   = 400,
})

hl.config({
    render = {
        cm_enabled = true,
        cm_auto_hdr = 1,
    },
})

-- Defaults for hot-plug
hl.monitor({
    output      = "",
    mode        = "preferred",
    position    = "auto-center-right",
    scale       = "auto",
    mirror      = "eDP-1",
})
