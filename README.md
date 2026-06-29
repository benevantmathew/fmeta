# fmeta - File Metadata Scanner

`fmeta` is a lightweight tool to scan directories and list file metadata in a tabular format.
It supports sorting, GUI mode, persistent GUI settings, and per-run UI overrides.

## Features
- Scan a folder and list file metadata: path, size, created time, modified time, and file type.
- Sort files by `Size (MB)`, `Path`, `Created`, `Modified`, or `File Type`.
- GUI-first workflow for interactive browsing.
- User-editable settings file for theme, main-window font, and result-window font.
- Result-window-only zoom with keyboard shortcuts.

## Installation
Install `fmeta` using pip:
```sh
pip install fmeta
```

For local development from this repository:
```sh
pip install -e .
```

## Example Usage

### Launch GUI for interactive file browsing
```sh
fmeta
```

### Scan a folder and display file details in a table
```sh
fmeta /path/to/directory
```

### Sort files by a metadata column
```sh
fmeta --sort "Created" /path/to/directory
```

### Override UI settings for a single run
```sh
fmeta --theme light --font_size 13 --result_font_size 14 --zoom 1.25 /path/to/directory
```

## Settings File

On first GUI launch, `fmeta` creates:

```text
~/.config/fmeta/settings.json
```

Edit this file to persist GUI preferences:

```json
{
    "ui": {
        "theme": "dark",
        "font_family": "Arial",
        "font_size": 12,
        "result_font_family": "Arial",
        "result_font_size": 12,
        "tk_scaling": 1.15,
        "window_width": 560,
        "window_height": 280,
        "popup_width": 1000,
        "popup_height": 520
    }
}
```

Supported themes are `dark` and `light`. Color keys can also be added to the `ui` object to override the built-in palette.

## Result Window Zoom

Zoom affects only the currently open result window.

- `Ctrl++` or `Ctrl+=`: increase result table font size
- `Ctrl+-`: decrease result table font size
- `Ctrl+0`: reset result table font size

## Metadata Columns

- `Path`
- `Size (MB)`
- `Created`
- `Modified`
- `File Type`
