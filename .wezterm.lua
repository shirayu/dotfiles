
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.font = wezterm.font 'VL Gothic'
config.color_scheme = 'Tango (terminal.sexy)'
config.font_size = 14

config.window_padding = {
    left = 0,
    right = 0,
    top = 0,
    bottom = 0,
}

config.enable_tab_bar = false
config.hyperlink_rules = {}
return config
