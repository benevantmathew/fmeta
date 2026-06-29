"""
Settings helpers for fmeta GUI.
"""
import json
import os
import shutil
import importlib.resources

DEFAULT_UI_SETTINGS = {
    "theme": "dark",
    "font_family": "Arial",
    "font_size": 12,
    "result_font_family": "Arial",
    "result_font_size": 12,
    "tk_scaling": 1.15,
    "window_width": 560,
    "window_height": 280,
    "popup_width": 1000,
    "popup_height": 520,
}

THEME_COLORS = {
    "dark": {
        "background_color": "#1e1e1e",
        "foreground_color": "#f2f2f2",
        "input_background_color": "#2d2d2d",
        "input_foreground_color": "#ffffff",
        "button_background_color": "#3a3a3a",
        "button_foreground_color": "#ffffff",
        "accent_color": "#2563eb",
        "result_background_color": "#111827",
        "result_foreground_color": "#f9fafb",
        "tree_heading_background_color": "#374151",
        "tree_heading_foreground_color": "#f9fafb",
        "scrollbar_background_color": "#2d2d2d",
    },
    "light": {
        "background_color": "#f4f4f5",
        "foreground_color": "#111827",
        "input_background_color": "#ffffff",
        "input_foreground_color": "#111827",
        "button_background_color": "#e5e7eb",
        "button_foreground_color": "#111827",
        "accent_color": "#bfdbfe",
        "result_background_color": "#ffffff",
        "result_foreground_color": "#111827",
        "tree_heading_background_color": "#dbeafe",
        "tree_heading_foreground_color": "#111827",
        "scrollbar_background_color": "#e5e7eb",
    },
}

COLOR_KEYS = tuple(next(iter(THEME_COLORS.values())).keys())


def get_user_settings_path():
    """
    Return the user-editable settings path, creating ~/.config/fmeta if needed.
    """
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "fmeta")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "settings.json")


def ensure_user_settings(settings_path=None):
    """
    Copy bundled default settings to the user config folder if missing.
    """
    settings_path = settings_path or get_user_settings_path()
    if os.path.exists(settings_path):
        return settings_path

    try:
        resource = importlib.resources.files("fmeta.application").joinpath("settings.json")
        with importlib.resources.as_file(resource) as src:
            shutil.copy2(src, settings_path)
    except (FileNotFoundError, ModuleNotFoundError, OSError):
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump({"ui": DEFAULT_UI_SETTINGS}, f, indent=4)
    return settings_path


def _positive_int(value, default_value):
    try:
        int_value = int(value)
    except (TypeError, ValueError):
        return default_value
    return int_value if int_value > 0 else default_value


def _positive_float(value, default_value):
    try:
        float_value = float(value)
    except (TypeError, ValueError):
        return default_value
    return float_value if float_value > 0 else default_value


def _normalize_theme(value):
    theme = str(value or DEFAULT_UI_SETTINGS["theme"]).strip().lower()
    return theme if theme in THEME_COLORS else DEFAULT_UI_SETTINGS["theme"]


def load_ui_settings(settings_path=None, overrides=None):
    """
    Load UI settings from JSON and apply optional non-persistent overrides.
    """
    settings_path = ensure_user_settings(settings_path)
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        data = {}

    file_settings = data.get("ui", {}) if isinstance(data, dict) else {}
    if not isinstance(file_settings, dict):
        file_settings = {}

    theme = _normalize_theme(file_settings.get("theme", DEFAULT_UI_SETTINGS["theme"]))
    if overrides and overrides.get("theme") is not None:
        theme = _normalize_theme(overrides["theme"])

    settings = DEFAULT_UI_SETTINGS.copy()
    settings.update(THEME_COLORS[theme])
    settings.update(file_settings)

    for key, value in (overrides or {}).items():
        if value is not None:
            settings[key] = value

    settings["theme"] = _normalize_theme(settings.get("theme"))
    if settings["theme"] != theme:
        explicit_colors = {
            key: settings[key]
            for key in COLOR_KEYS
            if key in file_settings or (overrides or {}).get(key) is not None
        }
        settings.update(THEME_COLORS[settings["theme"]])
        settings.update(explicit_colors)

    settings["font_family"] = str(settings.get("font_family") or DEFAULT_UI_SETTINGS["font_family"])
    settings["result_font_family"] = str(
        settings.get("result_font_family") or settings["font_family"]
    )
    for key in [
        "font_size",
        "result_font_size",
        "window_width",
        "window_height",
        "popup_width",
        "popup_height",
    ]:
        settings[key] = _positive_int(settings.get(key), DEFAULT_UI_SETTINGS[key])
    settings["tk_scaling"] = _positive_float(
        settings.get("tk_scaling"), DEFAULT_UI_SETTINGS["tk_scaling"]
    )
    for key in COLOR_KEYS:
        settings[key] = str(settings.get(key) or THEME_COLORS[settings["theme"]][key])
    return settings
