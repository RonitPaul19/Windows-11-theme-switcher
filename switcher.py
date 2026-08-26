#!/usr/bin/env python3

import ctypes
import json
import os
import re
import subprocess
import sys
from pathlib import Path


# ============================================================
# Paths
# ============================================================

HOME = Path.home()
SCRIPT_DIR = Path(__file__).resolve().parent

TERMINAL_CONFIG = (
    HOME
    / "AppData/Local/Packages/"
    / "Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json"
)

VSCODE_CONFIG = HOME / "AppData/Roaming/Code/User/settings.json"

YASB_CSS = HOME / ".config/yasb/styles.css"

GLAZEWM_CONFIG = HOME / ".glzr/glazewm/config.yaml"

GLAZEWM_CLI = (
    Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    / "glzr.io"
    / "GlazeWM"
    / "cli"
    / "glazewm.exe"
)

NEOVIM_CONFIG = HOME / "AppData/Local/nvim"
NEOVIM_STATE = NEOVIM_CONFIG / "lua/_theme_state.lua"

FLOWLAUNCHER_SETTINGS = HOME / "AppData/Roaming/FlowLauncher/Settings/Settings.json"

FLOWLAUNCHER_EXE = HOME / "AppData/Local/FlowLauncher/Flow.Launcher.exe"


# ============================================================
# Theme CSS
# ============================================================

ROSE_PINE_CSS = """:root {
        --accent: #c4a7e7;
        --alert-bg: rgb(246, 193, 119);
        --alert-border: rgb(246, 193, 119);
        --alert-text: rgb(144, 140, 170);
        --base: #191724;
        --black: #000000;
        --blue: #9ccfd8;
        --border-dark: #21202e;
        --btn-hover-bg: rgb(224, 222, 244);
        --button-bg: #26233a;
        --button-hover: rgb(224, 222, 244);
        --button-pressed: #403d52;
        --calendar-bg: rgb(31, 29, 46);
        --calendar-text: rgb(144, 140, 170);
        --cancel-icon: rgb(235, 111, 146);
        --cancel-label: rgb(235, 111, 146);
        --card-bg: rgb(31, 29, 46);
        --chart: #f6c177;
        --day-active-bg: rgb(33, 32, 46);
        --day-active-border: rgb(64, 61, 82);
        --disabled: #524f67;
        --edge: #9ccfd8;
        --firefox: #eb6f92;
        --gray: #6e6a86;
        --green: #31748f;
        --groove-hover: rgb(224, 222, 244);
        --hourly-bg: #31748f;
        --icon-dim: rgb(224, 222, 244);
        --lavender: #c4a7e7;
        --maroon: #eb6f92;
        --mauve: #c4a7e7;
        --media-bg: rgb(31, 29, 46);
        --muted: #6e6a86;
        --muted-alt: #908caa;
        --paused: #6e6a86;
        --popup-bg: rgb(31, 29, 46);
        --popup-hover: rgb(38, 35, 58);
        --spotify: #31748f;
        --subtext0: #e0def4;
        --subtext1: #e0def4;
        --surface0: #1f1d2e;
        --surface1: #26233a;
        --surface2: #403d52;
        --teal: #ebbcba;
        --text: #e0def4;
        --text-dim: rgb(224, 222, 244);
        --text-muted: rgb(144, 140, 170);
        --transparent: #191724;
        --transparent-base: #191724;
        --transparent-dark: #191724;
    --weather-bg: rgb(25, 23, 36);
    --white: #ffffff;
        --yellow: #f6c177;
            }"""


CATPPUCCIN_CSS = """:root {
        --accent: #cba6f7;
        --alert-bg: rgb(249, 226, 175);
        --alert-border: rgb(249, 226, 175);
        --alert-text: rgb(166, 173, 200);
        --base: #1e1e2e;
        --black: #000000;
        --blue: #89b4fa;
        --border-dark: #181825;
        --btn-hover-bg: rgb(181, 190, 254);
        --button-bg: #45475a;
        --button-hover: rgb(181, 190, 254);
        --button-pressed: #585b70;
        --calendar-bg: rgb(49, 50, 68);
        --calendar-text: rgb(166, 173, 200);
        --cancel-icon: rgb(243, 139, 168);
        --cancel-label: rgb(243, 139, 168);
        --card-bg: rgb(49, 50, 68);
        --chart: #fab387;
        --day-active-bg: rgb(33, 34, 44);
        --day-active-border: rgb(69, 71, 90);
        --disabled: #585b70;
        --edge: #89b4fa;
        --firefox: #f38ba8;
        --gray: #6c7086;
        --green: #a6e3a1;
        --groove-hover: rgb(181, 190, 254);
        --hourly-bg: #a6e3a1;
        --icon-dim: rgb(205, 214, 244);
        --lavender: #b4befe;
        --maroon: #eba0ac;
        --mauve: #cba6f7;
        --media-bg: rgb(49, 50, 68);
        --muted: #6c7086;
        --muted-alt: #7f849c;
        --paused: #6c7086;
        --popup-bg: rgb(49, 50, 68);
        --popup-hover: rgb(69, 71, 90);
        --spotify: #a6e3a1;
        --subtext0: #a6adc8;
        --subtext1: #bac2de;
        --surface0: #313244;
        --surface1: #45475a;
        --surface2: #585b70;
        --teal: #94e2d5;
        --text: #cdd6f4;
        --text-dim: rgb(205, 214, 244);
        --text-muted: rgb(166, 173, 200);
        --transparent: #1e1e2e;
        --transparent-base: #1e1e2e;
        --transparent-dark: #1e1e2e;
    --weather-bg: rgb(30, 30, 46);
    --white: #ffffff;
        --yellow: #f9e2af;
            }"""


EVERFOREST_CSS = """:root {
        --accent: #d699b6;
        --alert-bg: rgb(219, 188, 127);
        --alert-border: rgb(219, 188, 127);
        --alert-text: rgb(133, 146, 137);
        --base: #2d353b;
        --black: #000000;
        --blue: #7fbbb3;
        --border-dark: #232a2e;
        --btn-hover-bg: rgb(211, 198, 170);
        --button-bg: #4f585e;
        --button-hover: rgb(211, 198, 170);
        --button-pressed: #5c6a72;
        --calendar-bg: rgb(61, 72, 77);
        --calendar-text: rgb(133, 146, 137);
        --cancel-icon: rgb(230, 126, 128);
        --cancel-label: rgb(230, 126, 128);
        --card-bg: rgb(61, 72, 77);
        --chart: #e69875;
        --day-active-bg: rgb(45, 53, 59);
        --day-active-border: rgb(79, 88, 94);
        --disabled: #5c6a72;
        --edge: #7fbbb3;
        --firefox: #e67e80;
        --gray: #859289;
        --green: #a7c080;
        --groove-hover: rgb(211, 198, 170);
        --hourly-bg: #a7c080;
        --icon-dim: rgb(211, 198, 170);
        --lavender: #d699b6;
        --maroon: #e67e80;
        --mauve: #d699b6;
        --media-bg: rgb(61, 72, 77);
        --muted: #859289;
        --muted-alt: #9da9a0;
        --paused: #859289;
        --popup-bg: rgb(61, 72, 77);
        --popup-hover: rgb(79, 88, 94);
        --spotify: #a7c080;
        --subtext0: #d3c6aa;
        --subtext1: #d3c6aa;
        --surface0: #3d484d;
        --surface1: #4f585e;
        --surface2: #5c6a72;
        --teal: #83c092;
        --text: #d3c6aa;
        --text-dim: rgb(211, 198, 170);
        --text-muted: rgb(133, 146, 137);
        --transparent: #2d353b;
        --transparent-base: #2d353b;
        --transparent-dark: #2d353b;
    --weather-bg: rgb(45, 53, 59);
    --white: #ffffff;
        --yellow: #dbbc7f;
            }"""


NOIR_CSS = """:root {
        --accent: #ffffff;
        --alert-bg: rgb(255, 255, 255);
        --alert-border: rgb(255, 255, 255);
        --alert-text: rgb(0, 0, 0);
        --base: #000000;
        --black: #ffffff;
        --blue: #ffffff;
        --border-dark: #ffffff;
        --btn-hover-bg: rgb(255, 255, 255);
        --button-bg: #000000;
        --button-hover: rgb(255, 255, 255);
        --button-pressed: #ffffff;
        --calendar-bg: rgb(0, 0, 0);
        --calendar-text: rgb(255, 255, 255);
        --cancel-icon: rgb(255, 255, 255);
        --cancel-label: rgb(255, 255, 255);
        --card-bg: rgb(0, 0, 0);
        --chart: #ffffff;
        --day-active-bg: rgb(0, 0, 0);
        --day-active-border: rgb(255, 255, 255);
        --disabled: #555555;
        --edge: #ffffff;
        --firefox: #ffffff;
        --gray: #ffffff;
        --green: #ffffff;
        --groove-hover: rgb(255, 255, 255);
        --hourly-bg: #ffffff;
        --icon-dim: rgb(128, 128, 128);
        --lavender: #ffffff;
        --maroon: #ffffff;
        --mauve: #ffffff;
        --media-bg: rgb(0, 0, 0);
        --muted: #777777;
        --muted-alt: #999999;
        --paused: #777777;
        --popup-bg: rgb(0, 0, 0);
        --popup-hover: rgb(255, 255, 255);
        --spotify: #ffffff;
        --subtext0: #cccccc;
        --subtext1: #ffffff;
        --surface0: #000000;
        --surface1: #ffffff;
        --surface2: #555555;
        --teal: #ffffff;
        --text: #ffffff;
        --text-dim: rgb(200, 200, 200);
        --text-muted: rgb(128, 128, 128);
        --transparent: #000000;
        --transparent-base: #000000;
        --transparent-dark: #000000;
    --weather-bg: rgb(0, 0, 0);
    --white: #000000;
        --yellow: #ffffff;
            }"""


EINK_CSS = """:root {
        --accent: #ffffff;
        --alert-bg: rgb(20, 20, 20);
        --alert-border: rgb(55, 55, 55);
        --alert-text: rgb(255, 255, 255);
        --base: #000000;
        --black: #ffffff;
        --blue: #ffffff;
        --border-dark: #2f2f2f;
        --btn-hover-bg: rgb(55, 55, 55);
        --button-bg: #171717;
        --button-hover: rgb(55, 55, 55);
        --button-pressed: #2f2f2f;
        --calendar-bg: rgb(10, 10, 10);
        --calendar-text: rgb(255, 255, 255);
        --cancel-icon: rgb(255, 255, 255);
        --cancel-label: rgb(255, 255, 255);
        --card-bg: rgb(10, 10, 10);
        --chart: #ffffff;
        --day-active-bg: rgb(20, 20, 20);
        --day-active-border: rgb(55, 55, 55);
        --disabled: #555555;
        --edge: #ffffff;
        --firefox: #ffffff;
        --gray: #777777;
        --green: #ffffff;
        --groove-hover: rgb(55, 55, 55);
        --hourly-bg: #ffffff;
        --icon-dim: rgb(175, 175, 175);
        --lavender: #ffffff;
        --maroon: #ffffff;
        --mauve: #ffffff;
        --media-bg: rgb(10, 10, 10);
        --muted: #666666;
        --muted-alt: #888888;
        --paused: #666666;
        --popup-bg: rgb(5, 5, 5);
        --popup-hover: rgb(20, 20, 20);
        --spotify: #ffffff;
        --subtext0: #cccccc;
        --subtext1: #ffffff;
        --surface0: #0f0f0f;
        --surface1: #171717;
        --surface2: #2f2f2f;
        --teal: #ffffff;
        --text: #ffffff;
        --text-dim: rgb(195, 195, 195);
        --text-muted: rgb(135, 135, 135);
        --transparent: #000000;
        --transparent-base: #000000;
        --transparent-dark: #000000;
    --weather-bg: rgb(0, 0, 0);
    --white: #000000;
        --yellow: #ffffff;
            }"""


TOKYO_NIGHT_CSS = """:root {
        --accent: #bb9af7;
        --alert-bg: rgb(224, 175, 104);
        --alert-border: rgb(224, 175, 104);
        --alert-text: rgb(169, 177, 214);
        --base: #1a1b26;
        --black: #000000;
        --blue: #7aa2f7;
        --border-dark: #1f2335;
        --btn-hover-bg: rgb(192, 202, 245);
        --button-bg: #24283b;
        --button-hover: rgb(192, 202, 245);
        --button-pressed: #3b4261;
        --calendar-bg: rgb(31, 35, 53);
        --calendar-text: rgb(169, 177, 214);
        --cancel-icon: rgb(247, 118, 142);
        --cancel-label: rgb(247, 118, 142);
        --card-bg: rgb(31, 35, 53);
        --chart: #ff9e64;
        --day-active-bg: rgb(26, 27, 38);
        --day-active-border: rgb(59, 66, 97);
        --disabled: #565f89;
        --edge: #7aa2f7;
        --firefox: #f7768e;
        --gray: #565f89;
        --green: #9ece6a;
        --groove-hover: rgb(192, 202, 245);
        --hourly-bg: #9ece6a;
        --icon-dim: rgb(192, 202, 245);
        --lavender: #bb9af7;
        --maroon: #f7768e;
        --mauve: #bb9af7;
        --media-bg: rgb(31, 35, 53);
        --muted: #565f89;
        --muted-alt: #6f7bb6;
        --paused: #565f89;
        --popup-bg: rgb(31, 35, 53);
        --popup-hover: rgb(36, 40, 59);
        --spotify: #9ece6a;
        --subtext0: #a9b1d6;
        --subtext1: #c0caf5;
        --surface0: #1f2335;
        --surface1: #24283b;
        --surface2: #3b4261;
        --teal: #1abc9c;
        --text: #c0caf5;
        --text-dim: rgb(192, 202, 245);
        --text-muted: rgb(169, 177, 214);
        --transparent: #1a1b26;
        --transparent-base: #1a1b26;
        --transparent-dark: #1a1b26;
    --weather-bg: rgb(26, 27, 38);
    --white: #ffffff;
        --yellow: #e0af68;
            }"""


KANAGAWA_CSS = """:root {
        --accent: #957FB8;
        --alert-bg: rgb(230, 195, 132);
        --alert-border: rgb(230, 195, 132);
        --alert-text: rgb(200, 192, 147);
        --base: #1F1F28;
        --black: #000000;
        --blue: #7E9CD8;
        --border-dark: #2A2A37;
        --btn-hover-bg: rgb(220, 215, 186);
        --button-bg: #363646;
        --button-hover: rgb(220, 215, 186);
        --button-pressed: #54546D;
        --calendar-bg: rgb(31, 31, 40);
        --calendar-text: rgb(200, 192, 147);
        --cancel-icon: rgb(228, 104, 118);
        --cancel-label: rgb(228, 104, 118);
        --card-bg: rgb(31, 31, 40);
        --chart: #E6C384;
        --day-active-bg: rgb(31, 31, 40);
        --day-active-border: rgb(84, 84, 109);
        --disabled: #54546D;
        --edge: #7E9CD8;
        --firefox: #E46876;
        --gray: #727169;
        --green: #98BB6C;
        --groove-hover: rgb(220, 215, 186);
        --hourly-bg: #98BB6C;
        --icon-dim: rgb(220, 215, 186);
        --lavender: #957FB8;
        --maroon: #C34043;
        --mauve: #957FB8;
        --media-bg: rgb(31, 31, 40);
        --muted: #727169;
        --muted-alt: #938AA9;
        --paused: #727169;
        --popup-bg: rgb(31, 31, 40);
        --popup-hover: rgb(54, 54, 70);
        --spotify: #98BB6C;
        --subtext0: #DCD7BA;
        --subtext1: #DCD7BA;
        --surface0: #2A2A37;
        --surface1: #363646;
        --surface2: #54546D;
        --teal: #7AA89F;
        --text: #DCD7BA;
        --text-dim: rgb(220, 215, 186);
        --text-muted: rgb(200, 192, 147);
        --transparent: #1F1F28;
        --transparent-base: #1F1F28;
        --transparent-dark: #1F1F28;
    --weather-bg: rgb(31, 31, 40);
    --white: #ffffff;
        --yellow: #E6C384;
            }"""


# ============================================================
# Themes
# ============================================================

THEMES = {
    "Catppuccin": {
        "terminal_scheme": "Catppuccin Mocha",
        "terminal_scheme_def": {
            "background": "#1E1E2E",
            "black": "#45475A",
            "blue": "#89B4FA",
            "brightBlack": "#585B70",
            "brightBlue": "#89B4FA",
            "brightCyan": "#94E2D5",
            "brightGreen": "#A6E3A1",
            "brightPurple": "#F5C2E7",
            "brightRed": "#F38BA8",
            "brightWhite": "#A6ADC8",
            "brightYellow": "#F9E2AF",
            "cursorColor": "#F5E0DC",
            "cyan": "#89DCEB",
            "foreground": "#CDD6F4",
            "green": "#A6E3A1",
            "name": "Catppuccin Mocha",
            "purple": "#CBA6F7",
            "red": "#F38BA8",
            "selectionBackground": "#585B70",
            "white": "#BAC2DE",
            "yellow": "#F9E2AF",
        },
        "vscode_theme": "Catppuccin Mocha",
        "cursor_color": "#F5E0DC",
        "glazewm_focused": "#89B4FA",
        "glazewm_other": "#585B70",
        "wallpaper": SCRIPT_DIR / "wallpapers" / "catppuccin.jpg",
        "yasb_css": CATPPUCCIN_CSS,
        "neovim_theme": "catppuccin",
        "flowlauncher_theme": "CatppuccinMocha",
    },
    "RosePine": {
        "terminal_scheme": "Rose Pine",
        "terminal_scheme_def": {
            "background": "#191724",
            "black": "#26233A",
            "blue": "#9CCFD8",
            "brightBlack": "#6E6A86",
            "brightBlue": "#9CCFD8",
            "brightCyan": "#9CCFD8",
            "brightGreen": "#9CCFD8",
            "brightPurple": "#C4A7E7",
            "brightRed": "#EB6F92",
            "brightWhite": "#E0DEF4",
            "brightYellow": "#F6C177",
            "cursorColor": "#E0DEF4",
            "cyan": "#9CCFD8",
            "foreground": "#E0DEF4",
            "green": "#31748F",
            "name": "Rose Pine",
            "purple": "#C4A7E7",
            "red": "#EB6F92",
            "selectionBackground": "#403D52",
            "white": "#E0DEF4",
            "yellow": "#F6C177",
        },
        "vscode_theme": "Rosé Pine",
        "cursor_color": "#6e6a86",
        "glazewm_focused": "#9CCFD8",
        "glazewm_other": "#A3AABE",
        "wallpaper": SCRIPT_DIR / "wallpapers" / "rose-pine.jpg",
        "yasb_css": ROSE_PINE_CSS,
        "neovim_theme": "rose-pine",
        "flowlauncher_theme": "RosePine",
    },
    "Everforest": {
        "terminal_scheme": "Everforest Dark",
        "terminal_scheme_def": {
            "background": "#2D353B",
            "black": "#475258",
            "blue": "#7FBBB3",
            "brightBlack": "#859289",
            "brightBlue": "#7FBBB3",
            "brightCyan": "#83C092",
            "brightGreen": "#A7C080",
            "brightPurple": "#D699B6",
            "brightRed": "#E67E80",
            "brightWhite": "#D3C6AA",
            "brightYellow": "#DBBC7F",
            "cursorColor": "#D3C6AA",
            "cyan": "#83C092",
            "foreground": "#D3C6AA",
            "green": "#A7C080",
            "name": "Everforest Dark",
            "purple": "#D699B6",
            "red": "#E67E80",
            "selectionBackground": "#4F585E",
            "white": "#D3C6AA",
            "yellow": "#DBBC7F",
        },
        "vscode_theme": "Everforest Pro Dark",
        "cursor_color": "#D3C6AA",
        "glazewm_focused": "#7FBBB3",
        "glazewm_other": "#4F585E",
        "wallpaper": SCRIPT_DIR / "wallpapers" / "everforest.png",
        "yasb_css": EVERFOREST_CSS,
        "neovim_theme": "everforest",
        "flowlauncher_theme": "Everforest",
    },
    "Noir": {
        "terminal_scheme": "Noir",
        "terminal_scheme_def": {
            "background": "#000000",
            "black": "#000000",
            "blue": "#FFFFFF",
            "brightBlack": "#555555",
            "brightBlue": "#FFFFFF",
            "brightCyan": "#FFFFFF",
            "brightGreen": "#FFFFFF",
            "brightPurple": "#FFFFFF",
            "brightRed": "#FFFFFF",
            "brightWhite": "#FFFFFF",
            "brightYellow": "#FFFFFF",
            "cursorColor": "#FFFFFF",
            "cyan": "#FFFFFF",
            "foreground": "#FFFFFF",
            "green": "#FFFFFF",
            "name": "Noir",
            "purple": "#FFFFFF",
            "red": "#FFFFFF",
            "selectionBackground": "#333333",
            "white": "#FFFFFF",
            "yellow": "#FFFFFF",
        },
        "vscode_theme": "Monochrome Dark",
        "cursor_color": "#FFFFFF",
        "glazewm_focused": "#808080",
        "glazewm_other": "#333333",
        "wallpaper": SCRIPT_DIR / "wallpapers" / "eink.jpg",
        "yasb_css": NOIR_CSS,
        "neovim_theme": "noir",
        "flowlauncher_theme": "Noir",
    },
    "E-Ink": {
        "terminal_scheme": "E-Ink",
        "terminal_scheme_def": {
            "background": "#ffffff",
            "black": "#000000",
            "blue": "#FFFFFF",
            "brightBlack": "#555555",
            "brightBlue": "#FFFFFF",
            "brightCyan": "#FFFFFF",
            "brightGreen": "#FFFFFF",
            "brightPurple": "#FFFFFF",
            "brightRed": "#FFFFFF",
            "brightWhite": "#FFFFFF",
            "brightYellow": "#FFFFFF",
            "cursorColor": "#FFFFFF",
            "cyan": "#FFFFFF",
            "foreground": "#FFFFFF",
            "green": "#FFFFFF",
            "name": "E-Ink",
            "purple": "#FFFFFF",
            "red": "#FFFFFF",
            "selectionBackground": "#2F2F2F",
            "white": "#FFFFFF",
            "yellow": "#FFFFFF",
        },
        "vscode_theme": "E-Ink",
        "cursor_color": "#ffffff",
        "glazewm_focused": "#000000",
        "glazewm_other": "#999999",
        "wallpaper": SCRIPT_DIR / "wallpapers" / "eink.jpg",
        "yasb_css": EINK_CSS,
        "neovim_theme": "theink",
        "flowlauncher_theme": "Eink",
    },
    "Tokyo Night": {
        "terminal_scheme": "Tokyo Night",
        "terminal_scheme_def": {
            "background": "#1a1b26",
            "black": "#32344a",
            "blue": "#7aa2f7",
            "brightBlack": "#444b6a",
            "brightBlue": "#7aa2f7",
            "brightCyan": "#7dcfff",
            "brightGreen": "#9ece6a",
            "brightPurple": "#bb9af7",
            "brightRed": "#f7768e",
            "brightWhite": "#c0caf5",
            "brightYellow": "#e0af68",
            "cursorColor": "#c0caf5",
            "cyan": "#7dcfff",
            "foreground": "#c0caf5",
            "green": "#9ece6a",
            "name": "Tokyo Night",
            "purple": "#bb9af7",
            "red": "#f7768e",
            "selectionBackground": "#3b4261",
            "white": "#a9b1d6",
            "yellow": "#e0af68",
        },
        "vscode_theme": "Tokyo Night",
        "cursor_color": "#c0caf5",
        "glazewm_focused": "#7aa2f7",
        "glazewm_other": "#3b4261",
        "wallpaper": SCRIPT_DIR / "wallpapers" / "tokyo-night.jpg",
        "yasb_css": TOKYO_NIGHT_CSS,
        "neovim_theme": "tokyonight",
        "flowlauncher_theme": "Tokyonight",
    },
    "Kanagawa": {
        "terminal_scheme": "Kanagawa",
        "terminal_scheme_def": {
            "background": "#1F1F28",
            "black": "#16161D",
            "blue": "#7E9CD8",
            "brightBlack": "#727169",
            "brightBlue": "#7FB4CA",
            "brightCyan": "#7AA89F",
            "brightGreen": "#98BB6C",
            "brightPurple": "#938AA9",
            "brightRed": "#E82424",
            "brightWhite": "#DCD7BA",
            "brightYellow": "#E6C384",
            "cursorColor": "#DCD7BA",
            "cyan": "#6A9589",
            "foreground": "#DCD7BA",
            "green": "#76946A",
            "name": "Kanagawa",
            "purple": "#957FB8",
            "red": "#C34043",
            "selectionBackground": "#2D4F67",
            "white": "#C8C093",
            "yellow": "#C0A36E",
        },
        "vscode_theme": "Kanagawa",
        "cursor_color": "#DCD7BA",
        "glazewm_focused": "#7E9CD8",
        "glazewm_other": "#54546D",
        "wallpaper": SCRIPT_DIR / "wallpapers" / "kanagawa.jpg",
        "yasb_css": KANAGAWA_CSS,
        "neovim_theme": "kanagawa",
        "flowlauncher_theme": "Kanagawa",
    },
}


# ============================================================
# Helpers
# ============================================================


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def check_file(path: Path, name: str):
    if not path.exists():
        raise FileNotFoundError(f"{name} not found:\n{path}")


def strip_jsonc(text: str) -> str:
    result = []
    i = 0
    in_string = False
    escape = False

    while i < len(text):
        c = text[i]

        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False

            result.append(c)
            i += 1
            continue

        if c == '"':
            in_string = True
            result.append(c)
            i += 1
            continue

        if c == "/" and i + 1 < len(text):
            if text[i + 1] == "/":
                while i < len(text) and text[i] not in "\n\r":
                    i += 1
                continue

            if text[i + 1] == "*":
                i += 2

                while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1

                i += 2
                continue

        result.append(c)
        i += 1

    return "".join(result)


def json_parse(text: str):
    text = strip_jsonc(text)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return json.loads(text)


def update_json_file(path: Path, key: str, value):
    data = json_parse(read_file(path))
    data[key] = value

    write_file(
        path,
        json.dumps(data, indent=2, ensure_ascii=False),
    )

    return data


# ============================================================
# Windows Terminal
# ============================================================


def update_terminal_theme(
    scheme_name: str,
    cursor_color: str,
    scheme_def=None,
):
    check_file(TERMINAL_CONFIG, "Windows Terminal settings")

    data = json_parse(read_file(TERMINAL_CONFIG))

    data.setdefault("profiles", {}).setdefault("defaults", {})["colorScheme"] = (
        scheme_name
    )

    found = False

    for scheme in data.get("schemes", []):
        if scheme.get("name") == scheme_name:
            scheme["cursorColor"] = cursor_color
            found = True
            break

    if not found and scheme_def:
        scheme_def = scheme_def.copy()
        scheme_def["cursorColor"] = cursor_color
        data.setdefault("schemes", []).append(scheme_def)

    write_file(
        TERMINAL_CONFIG,
        json.dumps(data, indent=2, ensure_ascii=False),
    )

    print(f"  Terminal scheme       -> {scheme_name}")
    print(f"  Terminal cursor       -> {cursor_color}")


# ============================================================
# VS Code
# ============================================================


def update_vscode_theme(theme_name: str):
    check_file(VSCODE_CONFIG, "VS Code settings")

    data = json_parse(read_file(VSCODE_CONFIG))
    data["workbench.colorTheme"] = theme_name

    write_file(
        VSCODE_CONFIG,
        json.dumps(data, indent=2, ensure_ascii=False),
    )

    print(f"  VS Code theme         -> {theme_name}")


def update_vscode_terminal_cursor(
    theme_name: str,
    cursor_color: str,
):
    data = json_parse(read_file(VSCODE_CONFIG))

    customizations = data.setdefault(
        "workbench.colorCustomizations",
        {},
    )

    theme_key = f"[{theme_name}]"

    theme_overrides = customizations.setdefault(
        theme_key,
        {},
    )

    theme_overrides["terminalCursor.foreground"] = cursor_color

    write_file(
        VSCODE_CONFIG,
        json.dumps(data, indent=2, ensure_ascii=False),
    )

    print(f"  VS Code cursor        -> {cursor_color}")


# ============================================================
# YASB
# ============================================================


def update_yasb_css(css_root: str):
    check_file(YASB_CSS, "YASB stylesheet")

    content = read_file(YASB_CSS)

    # Find the first complete :root { ... } block.
    match = re.search(
        r":root\s*\{(?:[^{}]|\{[^{}]*\})*\}",
        content,
        flags=re.DOTALL,
    )

    if not match:
        print("  ✗ YASB :root block not found")
        return

    new_content = content[: match.start()] + css_root + content[match.end() :]

    write_file(YASB_CSS, new_content)

    print("  ✓ YASB CSS updated")


# ============================================================
# Neovim
# ============================================================


def update_neovim_theme(neovim_theme: str):
    state_file = NEOVIM_STATE

    content = f'vim.g.theme_name = "{neovim_theme}"\n'

    write_file(state_file, content)

    print(f"  Neovim colorscheme    -> {neovim_theme}")


# ============================================================
# Wallpaper
# ============================================================


def set_wallpaper(image_path: Path):
    image_path = image_path.resolve()

    print(f"  Wallpaper path        -> {image_path}")

    if not image_path.is_file():
        print(f"  ✗ Wallpaper not found -> {image_path}")
        return

    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02

    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        str(image_path),
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
    )

    if result:
        print("  ✓ Wallpaper changed")
    else:
        error = ctypes.get_last_error()
        print(f"  ✗ Wallpaper change failed (error {error})")


# ============================================================
# Theme application
# ============================================================


def apply_theme(theme_name: str):
    theme = THEMES[theme_name]

    print()
    print("=" * 60)
    print(f"Applying theme: {theme_name}")
    print("=" * 60)

    try:
        set_wallpaper(
            theme["wallpaper"],
        )

        update_terminal_theme(
            theme["terminal_scheme"],
            theme["cursor_color"],
            theme.get("terminal_scheme_def"),
        )

        update_vscode_theme(
            theme["vscode_theme"],
        )

        update_vscode_terminal_cursor(
            theme["vscode_theme"],
            theme["cursor_color"],
        )

        update_yasb_css(
            theme["yasb_css"],
        )

        update_neovim_theme(
            theme["neovim_theme"],
        )

        print()
        print("✓ Theme applied successfully!")
        print()

    except FileNotFoundError as e:
        print()
        print("✗ Missing file:")
        print(e)
        print()

    except json.JSONDecodeError as e:
        print()
        print("✗ Invalid JSON configuration:")
        print(e)
        print()

    except Exception as e:
        print()
        print("✗ Theme switch failed:")
        print(f"{type(e).__name__}: {e}")
        print()


# ============================================================
# CLI
# ============================================================


def main():
    if len(sys.argv) < 2:
        print()
        print("Usage:")
        print("  theme <theme-name>")
        print()
        print("Available themes:")

        for theme in THEMES:
            print(f"  - {theme}")

        print()

        return 1

    theme_name = " ".join(sys.argv[1:])

    if theme_name not in THEMES:
        print()
        print(f"✗ Unknown theme: {theme_name}")
        print()
        print("Available themes:")

        for theme in THEMES:
            print(f"  - {theme}")

        print()

        return 1

    apply_theme(theme_name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
