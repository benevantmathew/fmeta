# Changelog

## Version 1.0.0 - 29-06-2026
- Added a bundled GUI settings file copied to `~/.config/fmeta/settings.json` on first launch.
- Added persistent theme and font settings for the main window and result window.
- Added per-run UI overrides: `--theme`, `--font_size`, `--result_font_size`, and `--zoom` / `--tk_scaling`.
- Added result-window-only zoom key bindings: `Ctrl++`, `Ctrl+=`, `Ctrl+-`, and `Ctrl+0`.
- Updated packaging to include bundled JSON settings.

## version 0.1.4 (Bugfix) - 15-11-2025
- add MANIFEST.in to upload LICENSE README.md CHANGELOG.md

## Version 0.1.3 (Bugfix) - 15-03-2025
- fixed the issue with wrong version output.

## Version 0.1.2 (Bugfix) - 15-03-2025
- pypi upload fixed

## Version 0.1.1 (Bugfix) - 15-03-2025
- Removed the requirement for `tkinter` in `setup.py`.
- Added a detailed description with usage instructions.

## Version 0.1.0 - 15-03-2025
- The app will list all the files in the input directory with their metadata.
