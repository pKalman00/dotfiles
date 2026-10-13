hl.config({
    input = {
        kb_layout  = "hu",
        kb_variant = "",
        kb_model   = "",
        kb_options = "",
        kb_rules   = "",
        repeat_delay = 270,
        repeat_rate  = 25,

        follow_mouse = 1,

        sensitivity = 0, -- -1.0 - 1.0, 0 means no modification.
        
        accel_profile = "flat",
        natural_scroll = false,
    },
})

hl.device({
    name = "asup1415:00-093a:300c-touchpad",
    sensitivity = 0,
    natural_scroll = true,
    disable_while_typing = true,
    accel_profile = "adaptive"
})

hl.gesture({
    fingers = 3,
    direction = "horizontal",
    action = "workspace"
})

