#!/usr/bin/env python3
import json
import re
import subprocess
import sys
import ctypes
from pathlib import Path

TERMINAL_CONFIG = Path.home() / "AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json"
VSCODE_CONFIG = Path.home() / "AppData/Roaming/Code/User/settings.json"
YASB_CSS = Path.home() / ".config/yasb/styles.css"
GLAZEWM_CONFIG = Path.home() / ".glzr/glazewm/config.yaml"
GLAZEWM_CLI = "C:/Program Files/glzr.io/GlazeWM/cli/glazewm.exe"
NEOVIM_CONFIG = Path.home() / "AppData/Local/nvim"
NEOVIM_STATE = NEOVIM_CONFIG / "lua/_theme_state.lua"

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
    --accent: #999999;
    --alert-bg: rgb(128, 128, 128);
    --alert-border: rgb(128, 128, 128);
    --alert-text: rgb(192, 192, 192);
    --base: #0a0a0a;
    --black: #000000;
    --blue: #808080;
    --border-dark: #141414;
    --btn-hover-bg: rgb(200, 200, 200);
    --button-bg: #2a2a2a;
    --button-hover: rgb(200, 200, 200);
    --button-pressed: #333333;
    --calendar-bg: rgb(20, 20, 20);
    --calendar-text: rgb(128, 128, 128);
    --cancel-icon: rgb(128, 128, 128);
    --cancel-label: rgb(128, 128, 128);
    --card-bg: rgb(20, 20, 20);
    --chart: #808080;
    --day-active-bg: rgb(15, 15, 15);
    --day-active-border: rgb(42, 42, 42);
    --disabled: #333333;
    --edge: #808080;
    --firefox: #808080;
    --gray: #666666;
    --green: #808080;
    --groove-hover: rgb(200, 200, 200);
    --hourly-bg: #808080;
    --icon-dim: rgb(192, 192, 192);
    --lavender: #999999;
    --maroon: #808080;
    --mauve: #999999;
    --media-bg: rgb(20, 20, 20);
    --muted: #666666;
    --muted-alt: #808080;
    --paused: #666666;
    --popup-bg: rgb(20, 20, 20);
    --popup-hover: rgb(42, 42, 42);
    --spotify: #808080;
    --subtext0: #c0c0c0;
    --subtext1: #c0c0c0;
    --surface0: #1a1a1a;
    --surface1: #2a2a2a;
    --surface2: #333333;
    --teal: #808080;
    --text: #e0e0e0;
    --text-dim: rgb(192, 192, 192);
    --text-muted: rgb(128, 128, 128);
    --transparent: #0a0a0a;
    --transparent-base: #0a0a0a;
    --transparent-dark: #0a0a0a;
    --weather-bg: rgb(10, 10, 10);
    --white: #ffffff;
    --yellow: #808080;
}"""

THEMES = {
    "Catppuccin": {
        "terminal_scheme": "Catppuccin Mocha",
        "vscode_theme": "Catppuccin Mocha",
        "glazewm_focused": "#89B4FA",
        "glazewm_other": "#585B70",
        "wallpaper": str(Path.home() / "Downloads/wallpapers/catppuccin.jpg"),
        "yasb_css": CATPPUCCIN_CSS,
        "neovim_theme": "catppuccin",
    },
    "RosePine": {
        "terminal_scheme": "Rose Pine",
        "vscode_theme": "Rosé Pine",
        "glazewm_focused": "#9CCFD8",
        "glazewm_other": "#A3AABE",
        "wallpaper": str(Path.home() / "Downloads/wallpapers/rose-pine.jpg"),
        "yasb_css": ROSE_PINE_CSS,
        "neovim_theme": "rose-pine",
    },
    "Everforest": {
        "terminal_scheme": "Everforest Dark",
        "vscode_theme": "Everforest Pro Dark",
        "glazewm_focused": "#7FBBB3",
        "glazewm_other": "#4F585E",
        "wallpaper": str(Path.home() / "Downloads/wallpapers/everforsest.png"),
        "yasb_css": EVERFOREST_CSS,
        "neovim_theme": "everforest",
    },
    "Noir": {
        "terminal_scheme": "Noir",
        "vscode_theme": "Monochrome Dark",
        "glazewm_focused": "#808080",
        "glazewm_other": "#333333",
        "wallpaper": str(Path.home() / "Downloads/wallpapers/noir.jpg"),
        "yasb_css": NOIR_CSS,
        "neovim_theme": "moonfly",
    },
}


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def json_parse(text):
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    return json.loads(text)


def update_json_file(path, key, value):
    content = read_file(path)
    data = json_parse(content)
    data[key] = value
    write_file(path, json.dumps(data, indent=2, ensure_ascii=False))
    return data


def update_terminal_theme(scheme_name):
    content = read_file(TERMINAL_CONFIG)
    data = json_parse(content)
    data["profiles"]["defaults"]["colorScheme"] = scheme_name
    write_file(TERMINAL_CONFIG, json.dumps(data, indent=2, ensure_ascii=False))
    print(f"  Terminal scheme -> {scheme_name}")


def update_vscode_theme(theme_name):
    content = read_file(VSCODE_CONFIG)
    data = json_parse(content)
    data["workbench.colorTheme"] = theme_name
    write_file(VSCODE_CONFIG, json.dumps(data, indent=2, ensure_ascii=False))
    print(f"  VSCode theme -> {theme_name}")


def update_yasb_css(css_root):
    content = read_file(YASB_CSS)
    content = re.sub(
        r':root\s*\{.*?\}',
        css_root,
        content,
        flags=re.DOTALL,
    )
    write_file(YASB_CSS, content)
    print(f"  YASB CSS updated")


def update_glazewm_border(focused_color, other_color):
    content = read_file(GLAZEWM_CONFIG)
    lines = content.split('\n')
    new_lines = []
    in_focused = False
    in_other = False
    for line in lines:
        stripped = line.strip()
        if stripped == 'focused_window:':
            in_focused = True
            in_other = False
        elif stripped == 'other_windows:':
            in_other = True
            in_focused = False
        elif stripped.startswith('color:'):
            if in_focused:
                line = re.sub(r"color:\s*'#[A-Fa-f0-9]+'", f"color: '{focused_color}'", line)
            elif in_other:
                line = re.sub(r"color:\s*'#[A-Fa-f0-9]+'", f"color: '{other_color}'", line)
        new_lines.append(line)

    write_file(GLAZEWM_CONFIG, '\n'.join(new_lines))
    print(f"  GlazeWM borders -> focused: {focused_color}, other: {other_color}")


def reload_glazewm():
    try:
        result = subprocess.run(
            [GLAZEWM_CLI, "command", "wm-reload-config"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            print("  GlazeWM config reloaded")
        else:
            print(f"  GlazeWM reload failed: {result.stderr}")
    except Exception as e:
        print(f"  GlazeWM reload error: {e}")


def update_neovim_theme(colorscheme):
    content = f'return "{colorscheme}"\n'
    write_file(NEOVIM_STATE, content)
    print(f"  Neovim theme -> {colorscheme}")
    try:
        subprocess.run(
            ["nvim", "--server", r"\\.\pipe\theme-switcher", "--remote-send",
             f":lua require('config.theme').load()<CR>"],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        pass


def set_wallpaper(image_path):
    image_path = str(Path(image_path).resolve())
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path,
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
    )
    print(f"  Wallpaper -> {image_path}")


def apply_theme(theme_name):
    theme = THEMES[theme_name]
    print(f"\nApplying theme: {theme_name}")

    update_terminal_theme(theme["terminal_scheme"])
    update_vscode_theme(theme["vscode_theme"])
    update_neovim_theme(theme["neovim_theme"])
    update_yasb_css(theme["yasb_css"])
    update_glazewm_border(theme["glazewm_focused"], theme["glazewm_other"])
    set_wallpaper(theme["wallpaper"])
    reload_glazewm()

    print(f"  Done!")


if __name__ == "__main__":
    theme_name = " ".join(sys.argv[1:])
    if theme_name in THEMES:
        apply_theme(theme_name)
    else:
        print("Usage:")
        print("  python switcher.py <theme-name>")
        print(f"Themes: {', '.join(THEMES.keys())}")
