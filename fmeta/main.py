import argparse
import os
import sys
import pandas as pd
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk

from fmeta.settings import load_ui_settings
from fmeta.version import __author__, __email__, __version__

# variable
size_col = "Size (MB)"
ALLOWED_SORT_COLUMNS = (size_col, "Path", "Created", "Modified", "File Type")


def _parse_args(argv):
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="fmeta",
        description="Scan directories and list file metadata in a tabular GUI.",
        add_help=False,
    )
    parser.add_argument("directory", nargs="?")
    parser.add_argument("--sort", default=size_col)
    parser.add_argument("--font_size", type=int)
    parser.add_argument("--result_font_size", type=int)
    parser.add_argument("--zoom", "--tk_scaling", dest="tk_scaling", type=float)
    parser.add_argument("--theme", choices=["dark", "light"])
    return parser.parse_args(argv)


# Function to display help
def print_help():
    help_message = """
Usage: fmeta [OPTIONS] [DIRECTORY]

A small package to scan directories and list file metadata in a tabular format.

Options:
    --version, -v           Show the version of fmeta and exit
    --author, -a            Show the author and exit
    --email, -e             Show the contact email and exit
    --help, -h              Show this help message and exit
    --sort COLUMN           Sort by the specified column
                            Columns: Size (MB), Path, Created, Modified, File Type
    --theme {dark,light}    Override the GUI theme for this run
    --font_size SIZE        Override the main window font size for this run
    --result_font_size SIZE Override the result window font size for this run
    --zoom SCALE            Override Tk scaling for this run

Settings:
    User-editable GUI settings are created at ~/.config/fmeta/settings.json.
    Edit that file to choose persistent theme, main-window font, and result-window font.

Result window zoom keys:
    Ctrl++ / Ctrl+=         Increase result table font size
    Ctrl+-                  Decrease result table font size
    Ctrl+0                  Reset result table font size

Arguments:
    (No arguments)          Launch the GUI application
    DIRECTORY               Launch GUI and scan the specified directory
"""
    print(help_message)
    sys.exit(0)


# Function to get file metadata
def get_file_metadata(folder, sort_by=size_col):
    file_data = []
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                stat = os.stat(file_path)
                file_data.append({
                    "Path": file_path,
                    size_col: round(stat.st_size / (1024 * 1024), 4),
                    "Created": pd.to_datetime(stat.st_ctime, unit="s").strftime("%Y-%m-%d %H:%M:%S"),
                    "Modified": pd.to_datetime(stat.st_mtime, unit="s").strftime("%Y-%m-%d %H:%M:%S"),
                    "File Type": os.path.splitext(file)[1]
                })
            except Exception as e:
                print(f"Error reading file: {file_path} - {e}")
    df = pd.DataFrame(file_data)
    if df.empty:
        return df
    if sort_by not in df.columns:
        sort_by = size_col
    return df.sort_values(by=sort_by, ascending=False)


def _apply_option_menu_theme(option_menu, settings):
    """
    Apply colors to tk.OptionMenu including its dropdown menu.
    """
    option_menu.configure(
        font=(settings["font_family"], settings["font_size"]),
        bg=settings["input_background_color"],
        fg=settings["input_foreground_color"],
        activebackground=settings["accent_color"],
        activeforeground=settings["button_foreground_color"],
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=0,
    )
    option_menu["menu"].configure(
        bg=settings["input_background_color"],
        fg=settings["input_foreground_color"],
        activebackground=settings["accent_color"],
        activeforeground=settings["button_foreground_color"],
    )


# GUI Application
def create_gui(initial_folder=None, sort_col=size_col, ui_options=None):
    ui_settings = load_ui_settings(overrides=ui_options)
    font_family = ui_settings["font_family"]
    normal_font = (font_family, ui_settings["font_size"])
    button_font = (font_family, ui_settings["font_size"], "bold")
    background_color = ui_settings["background_color"]
    foreground_color = ui_settings["foreground_color"]
    input_background_color = ui_settings["input_background_color"]
    input_foreground_color = ui_settings["input_foreground_color"]
    button_background_color = ui_settings["button_background_color"]
    button_foreground_color = ui_settings["button_foreground_color"]
    accent_color = ui_settings["accent_color"]

    def select_folder():
        path = filedialog.askdirectory(title="Select a Folder")
        if path:
            folder_var.set(path)

    def show_results(df):
        # Display results in a popup window
        popup = tk.Toplevel(root)
        popup.title("File Metadata Results")
        popup.geometry(f"{ui_settings['popup_width']}x{ui_settings['popup_height']}")
        popup.configure(bg=background_color)

        result_font_size = ui_settings["result_font_size"]
        result_font = tkfont.Font(
            root=popup,
            family=ui_settings["result_font_family"],
            size=result_font_size,
        )
        heading_font = tkfont.Font(
            root=popup,
            family=ui_settings["result_font_family"],
            size=result_font_size,
            weight="bold",
        )

        style = ttk.Style(popup)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        tree_style = "FMeta.Results.Treeview"
        style.configure(
            tree_style,
            font=result_font,
            rowheight=max(22, result_font_size + 12),
            background=ui_settings["result_background_color"],
            foreground=ui_settings["result_foreground_color"],
            fieldbackground=ui_settings["result_background_color"],
            borderwidth=0,
        )
        style.map(
            tree_style,
            background=[("selected", accent_color)],
            foreground=[("selected", ui_settings["result_foreground_color"])],
        )
        style.configure(
            f"{tree_style}.Heading",
            font=heading_font,
            background=ui_settings["tree_heading_background_color"],
            foreground=ui_settings["tree_heading_foreground_color"],
        )

        frame = tk.Frame(popup, bg=background_color)
        frame.pack(expand=True, fill=tk.BOTH, padx=8, pady=(8, 0))
        tree = ttk.Treeview(frame, columns=list(df.columns), show="headings", style=tree_style)
        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            width = 420 if col == "Path" else 160
            tree.column(col, width=width, anchor="w")

        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

        y_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        hint = tk.Label(
            popup,
            text="Result zoom: Ctrl++ / Ctrl+= to increase, Ctrl+- to decrease, Ctrl+0 to reset",
            font=(font_family, max(9, ui_settings["font_size"] - 2)),
            bg=background_color,
            fg=foreground_color,
        )
        hint.pack(fill=tk.X, padx=8, pady=6)

        current_result_font_size = {"value": result_font_size}

        def update_result_font(size):
            safe_size = max(8, min(72, int(size)))
            current_result_font_size["value"] = safe_size
            result_font.configure(size=safe_size)
            heading_font.configure(size=safe_size)
            style.configure(tree_style, rowheight=max(22, safe_size + 12))

        def zoom_result_font(direction):
            def zoom(_event):
                update_result_font(current_result_font_size["value"] + direction)
                return "break"
            return zoom

        def reset_result_font(_event):
            update_result_font(result_font_size)
            return "break"

        for widget in (popup, tree):
            widget.bind("<Control-plus>", zoom_result_font(1))
            widget.bind("<Control-equal>", zoom_result_font(1))
            widget.bind("<Control-KP_Add>", zoom_result_font(1))
            widget.bind("<Control-minus>", zoom_result_font(-1))
            widget.bind("<Control-KP_Subtract>", zoom_result_font(-1))
            widget.bind("<Control-0>", reset_result_font)
            widget.bind("<Control-KP_0>", reset_result_font)
        tree.focus_set()

    def scan():
        folder = folder_var.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder")
            return
        if not os.path.exists(folder):
            messagebox.showerror("Error", "Selected folder does not exist")
            return

        df = get_file_metadata(folder, sort_by=sort_option.get())
        file_count = len(df)

        if df.empty:
            messagebox.showinfo("No Files", "No files found in the selected directory.")
            return

        messagebox.showinfo("Scan Complete", f"Total files found: {file_count}")
        show_results(df)

    root = tk.Tk()
    root.tk.call("tk", "scaling", ui_settings["tk_scaling"])
    root.title("File Metadata Scanner")
    root.geometry(f"{ui_settings['window_width']}x{ui_settings['window_height']}")
    root.configure(bg=background_color)

    folder_var = tk.StringVar()
    sort_option = tk.StringVar(value=sort_col if sort_col in ALLOWED_SORT_COLUMNS else size_col)
    if initial_folder:
        folder_var.set(initial_folder)
        root.after(100, scan)  # Auto-scan after GUI loads

    label_options = {"font": normal_font, "bg": background_color, "fg": foreground_color}
    entry_options = {
        "width": 54,
        "font": normal_font,
        "bg": input_background_color,
        "fg": input_foreground_color,
        "insertbackground": input_foreground_color,
        "selectbackground": accent_color,
        "selectforeground": input_foreground_color,
        "relief": tk.FLAT,
    }
    button_options = {
        "font": normal_font,
        "bg": button_background_color,
        "fg": button_foreground_color,
        "activebackground": accent_color,
        "activeforeground": button_foreground_color,
        "relief": tk.FLAT,
        "borderwidth": 0,
        "padx": 8,
        "pady": 4,
    }

    tk.Label(root, text="Folder Path:", **label_options).pack(pady=5)
    tk.Entry(root, textvariable=folder_var, **entry_options).pack()
    tk.Button(root, text="Select Folder", command=select_folder, **button_options).pack(pady=5)

    tk.Label(root, text="Sort By:", **label_options).pack(pady=5)
    sort_menu = tk.OptionMenu(root, sort_option, *ALLOWED_SORT_COLUMNS)
    _apply_option_menu_theme(sort_menu, ui_settings)
    sort_menu.pack()

    scan_button_options = button_options.copy()
    scan_button_options.update({"font": button_font, "bg": accent_color})
    tk.Button(root, text="Scan Files", command=scan, **scan_button_options).pack(pady=20)

    root.mainloop()


# Main entry point
def main():
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"fmeta version {__version__}")
        sys.exit(0)

    if "--author" in sys.argv or "-a" in sys.argv:
        print(f"Author {__author__}")
        sys.exit(0)

    if "--email" in sys.argv or "-e" in sys.argv:
        print(f"Mailto {__email__}")
        sys.exit(0)

    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)

    args = _parse_args(sys.argv[1:])
    if args.sort not in ALLOWED_SORT_COLUMNS:
        print(f"Error: Invalid sort column '{args.sort}'.")
        print(f"Allowed columns: {', '.join(ALLOWED_SORT_COLUMNS)}")
        sys.exit(1)

    ui_options = {
        "font_size": args.font_size,
        "result_font_size": args.result_font_size,
        "tk_scaling": args.tk_scaling,
        "theme": args.theme,
    }

    if args.directory:
        if os.path.exists(args.directory):
            create_gui(initial_folder=args.directory, sort_col=args.sort, ui_options=ui_options)
        else:
            print(f"Error: Directory '{args.directory}' does not exist.")
            sys.exit(1)
    else:
        create_gui(sort_col=args.sort, ui_options=ui_options)


if __name__ == "__main__":
    main()
