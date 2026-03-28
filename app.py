import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from pathlib import Path
import webbrowser
import sys
import json
import ctypes

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / filename
    return Path(__file__).parent / filename

if hasattr(sys, '_MEIPASS'):
    HISTORY_FILE = Path(sys.executable).parent / "history.json"
else:
    HISTORY_FILE = Path(__file__).parent / "history.json"

PREVIEW_SIZE = 256

DISCORD_URL = "https://discord.gg/wbpgtKNSM7"
NAVY = "#0D47A1"
NAVY_DARK = "#0a3880"
RADIUS = 8

LIGHT = {
    "bg": "#f5f5f5",
    "fg": "#212121",
    "secondary_fg": "#757575",
    "accent": NAVY,
    "accent_fg": "#ffffff",
    "entry_bg": "#ffffff",
    "entry_fg": "#212121",
    "button_bg": NAVY,
    "button_fg": "#ffffff",
    "canvas_bg": "#e0e0e0",
    "frame_bg": "#ffffff",
    "border": "#e0e0e0",
    "footer_bg": "#eeeeee",
    "watermark": "light.png",
    "label_fg": "#212121",
    "sidebar_bg": "#e8e8e8",
    "sidebar_item": "#d0d0d0",
    "sidebar_selected": NAVY,
}

DARK = {
    "bg": "#121212",
    "fg": "#ffffff",
    "secondary_fg": "#aaaaaa",
    "accent": NAVY,
    "accent_fg": "#ffffff",
    "entry_bg": "#1e1e1e",
    "entry_fg": "#ffffff",
    "button_bg": NAVY,
    "button_fg": "#ffffff",
    "canvas_bg": "#2a2a2a",
    "frame_bg": "#1e1e1e",
    "border": "#2e2e2e",
    "footer_bg": "#1a1a1a",
    "watermark": "dark.png",
    "label_fg": "#ffffff",
    "sidebar_bg": "#1a1a1a",
    "sidebar_item": "#2a2a2a",
    "sidebar_selected": NAVY,
}

current_theme = DARK

root = tk.Tk()
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ppsspp.trt")
except:
    pass
try:
    icon_path = resource_path("chocobo2.ico")
    if icon_path.exists():
        root.iconbitmap(str(icon_path))
except:
    pass
root.title("PPSSPP Texture Replacement Tool")
root.geometry("1040x680")
root.resizable(False, False)

def load_font(filename):
    font_path = str(resource_path(filename))
    ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)
    return font_path

load_font("TrajanPro-Regular.ttf")
load_font("FuturaStd-Medium")
load_font("FuturaStd-Book.otf")

old_png_path = tk.StringVar()
new_png_path = tk.StringVar()
output_folder_path = tk.StringVar()
selected_category = tk.StringVar()
selected_category.set("")
selected_sub_category = tk.StringVar()
selected_sub_category.set("")
game_folder_path = tk.StringVar()
game_folder_path.set("")

old_img_ref = None
new_img_ref = None
old_img_full = None
new_img_full = None
side_img_ref = None
old_label_img = None
new_label_img = None
main_menu_img = None
theme_label_img = None
all_widgets = []
history_data = []
sidebar_sort = "recent"

FONT_TITLE = ("Trajan Pro", 14, "bold")
FONT_TITLE2 = ("Trajan Pro", 12)
FONT_HEADER = ("Futura Std Medium", 10, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 8)
FONT_BUTTON = ("Segoe UI", 9, "bold")
FONT_FOOTER = ("Futura Std Book", 8)
FONT_SIDEBAR = ("Futura Std Book", 8)

class Tooltip:
    def __init__(self, widget, text, delay=600):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._job = None
        self._win = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._cancel)

    def _schedule(self, event):
        self._cancel(event)
        self._job = self.widget.after(self.delay, self._show)

    def _cancel(self, event):
        if self._job:
            self.widget.after_cancel(self._job)
            self._job = None
        if self._win:
            self._win.destroy()
            self._win = None

    def _show(self):
        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._win = tk.Toplevel(self.widget)
        self._win.wm_overrideredirect(True)
        self._win.wm_geometry(f"+{x}+{y}")
        tk.Label(self._win, text=self.text, font=FONT_SMALL, bg="#ffffe0", fg="#333333",
                 relief="solid", borderwidth=1, padx=6, pady=4).pack()

def load_history():
    global history_data
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r") as f:
                history_data = json.load(f)
    except:
        history_data = []

def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history_data, f, indent=2)
    except:
        pass

def sort_history(method):
    global history_data, sidebar_sort
    sidebar_sort = method
    if method == "recent":
        history_data = sorted(history_data, key=lambda g: history_data.index(g))
        load_history()
        refresh_sidebar()
    elif method == "alpha_asc":
        history_data = sorted(history_data, key=lambda g: g["name"].lower())
        refresh_sidebar()
    elif method == "alpha_desc":
        history_data = sorted(history_data, key=lambda g: g["name"].lower(), reverse=True)
        refresh_sidebar()
    elif method == "last_added":
        history_data = list(reversed(history_data))
        refresh_sidebar()

def refresh_sidebar():
    for widget in sidebar_list_frame.winfo_children():
        widget.destroy()
    for i, game in enumerate(history_data):
        item_frame = tk.Frame(sidebar_list_frame, bg=current_theme["sidebar_item"], cursor="hand2", relief="flat", bd=0)
        item_frame.pack(fill="x", pady=2, padx=4, ipadx=4, ipady=2)
        display_name = game["name"]
        name_lbl = tk.Label(item_frame, text=display_name, font=FONT_SIDEBAR, bg=current_theme["sidebar_item"], fg=current_theme["fg"], anchor="w", justify="left", padx=8, pady=6)
        name_lbl.pack(fill="x")
        name_lbl.update_idletasks()
        max_width = sidebar_frame.winfo_width() - 24
        if name_lbl.winfo_reqwidth() > max_width:
            chars = list(game["name"])
            while len(chars) > 0:
                test = "".join(chars) + "..."
                name_lbl.config(text=test)
                name_lbl.update_idletasks()
                if name_lbl.winfo_reqwidth() <= max_width:
                    break
                chars.pop()
            if len(chars) == 0:
                name_lbl.config(text="...")
        def on_click(event, g=game):
            select_game(g)
        def on_enter(event, f=item_frame, l=name_lbl):
            f.config(bg=NAVY)
            l.config(bg=NAVY, fg="#ffffff")
        def on_leave(event, f=item_frame, l=name_lbl):
            f.config(bg=current_theme["sidebar_item"])
            l.config(bg=current_theme["sidebar_item"], fg=current_theme["fg"])
        def on_right_click(event, idx=i):
            show_context_menu(event, idx)
        item_frame.bind("<Button-1>", on_click)
        name_lbl.bind("<Button-1>", on_click)
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        name_lbl.bind("<Enter>", on_enter)
        name_lbl.bind("<Leave>", on_leave)
        item_frame.bind("<Button-3>", on_right_click)
        name_lbl.bind("<Button-3>", on_right_click)

def select_game(game):
    if game.get("ini_path"):
        output_folder_path.set(game["ini_path"])
        load_categories(game["ini_path"])
        cat_sub_frame.grid()
        category_frame.grid()
    if game.get("folder_path"):
        game_folder_path.set(game["folder_path"])

def show_context_menu(event, idx):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Rename", command=lambda: rename_game(idx))
    menu.add_command(label="Remove", command=lambda: remove_game(idx))
    menu.add_separator()
    sort_menu = tk.Menu(menu, tearoff=0)
    sort_menu.add_command(label="Recent", command=lambda: sort_history("recent"))
    sort_menu.add_command(label="Alphabetically (A-Z)", command=lambda: sort_history("alpha_asc"))
    sort_menu.add_command(label="Alphabetically (Z-A)", command=lambda: sort_history("alpha_desc"))
    sort_menu.add_command(label="Last Added", command=lambda: sort_history("last_added"))
    menu.add_cascade(label="Sort by", menu=sort_menu)
    menu.tk_popup(event.x_root, event.y_root)

def ask_string_borderless(title, prompt, initialvalue=""):
    result = [None]
    dialog = tk.Toplevel(root)
    dialog.overrideredirect(True)
    dialog.grab_set()
    dialog.config(bg=NAVY)
    dialog.update_idletasks()
    w, h = 360, 130
    x = root.winfo_rootx() + (root.winfo_width() - w) // 2
    y = root.winfo_rooty() + (root.winfo_height() - h) // 2
    dialog.geometry(f"{w}x{h}+{x}+{y}")

    inner = tk.Frame(dialog, bg=current_theme["bg"])
    inner.place(x=2, y=2, width=w-4, height=h-4)

    tk.Label(inner, text=prompt, font=FONT_BODY, bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=(14, 6), padx=16)
    entry = tk.Entry(inner, font=FONT_BODY, bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], relief="flat", highlightthickness=1, highlightbackground=NAVY, highlightcolor=NAVY)
    entry.pack(fill="x", padx=16)
    entry.insert(0, initialvalue)
    entry.select_range(0, tk.END)
    entry.focus_set()

    def confirm(e=None):
        result[0] = entry.get()
        dialog.destroy()
    def cancel(e=None):
        dialog.destroy()

    entry.bind("<Return>", confirm)
    entry.bind("<Escape>", cancel)

    btn_frame = tk.Frame(inner, bg=current_theme["bg"])
    btn_frame.pack(pady=8)
    make_rounded_button(btn_frame, "OK", confirm, width=60, height=28, parent_bg=current_theme["bg"]).pack(side="left", padx=4)
    make_rounded_button(btn_frame, "Cancel", cancel, width=60, height=28, bg="#555555", hover_bg="#333333", parent_bg=current_theme["bg"]).pack(side="left", padx=4)

    root.wait_window(dialog)
    return result[0]

def rename_game(idx):
    new_name = ask_string_borderless("Rename", "Enter new name:", initialvalue=history_data[idx]["name"])
    if new_name:
        history_data[idx]["name"] = new_name
        save_history()
        refresh_sidebar()

def remove_game(idx):
    if messagebox.askyesno("Remove", f"Remove '{history_data[idx]['name']}' from history?"):
        history_data.pop(idx)
        save_history()
        refresh_sidebar()

def add_game_to_history():
    folder = filedialog.askdirectory(title="Select game folder (e.g. ULES01505)")
    if not folder:
        return
    folder_path = Path(folder)
    ini_path = folder_path / "textures.ini"
    name = folder_path.name
    custom_name = ask_string_borderless("Game name", "Enter a display name for this game:", initialvalue=name)
    if not custom_name:
        custom_name = name
    existing = next((g for g in history_data if g["folder_path"] == str(folder_path)), None)
    if existing:
        messagebox.showinfo("Already exists", "This game folder is already in history.")
        return
    entry = {
        "name": custom_name,
        "folder_path": str(folder_path),
        "ini_path": str(ini_path) if ini_path.exists() else ""
    }
    history_data.append(entry)
    save_history()
    refresh_sidebar()

def make_rounded_button(parent, text, command, font=None, width=100, height=32, radius=RADIUS, bg=NAVY, fg="#ffffff", hover_bg=NAVY_DARK, parent_bg=None, cursor="hand2", pady=0, padx=0):
    if font is None:
        font = FONT_BUTTON
    if parent_bg is None:
        parent_bg = current_theme["bg"]
    c = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=parent_bg, cursor=cursor)
    def draw(color):
        c.delete("all")
        x1, y1, x2, y2 = 0, 0, width, height
        c.create_arc(x1, y1, x1+2*radius, y1+2*radius, start=90, extent=90, fill=color, outline=color)
        c.create_arc(x2-2*radius, y1, x2, y1+2*radius, start=0, extent=90, fill=color, outline=color)
        c.create_arc(x1, y2-2*radius, x1+2*radius, y2, start=180, extent=90, fill=color, outline=color)
        c.create_arc(x2-2*radius, y2-2*radius, x2, y2, start=270, extent=90, fill=color, outline=color)
        c.create_rectangle(x1+radius, y1, x2-radius, y2, fill=color, outline=color)
        c.create_rectangle(x1, y1+radius, x2, y2-radius, fill=color, outline=color)
        c.create_text(width//2, height//2, text=text, fill=fg, font=font)
    draw(bg)
    c.bind("<Enter>", lambda e: draw(hover_bg))
    c.bind("<Leave>", lambda e: draw(bg))
    c.bind("<Button-1>", lambda e: command())
    c._bg = bg
    c._hover_bg = hover_bg
    c._draw = draw
    c._parent_bg = parent_bg
    return c

def update_rounded_button_bg(canvas, parent_bg):
    canvas.config(bg=parent_bg)
    canvas._parent_bg = parent_bg
    canvas._draw(canvas._bg)

rounded_buttons = []

def make_vertical_label(text, color, fontsize=18):
    try:
        font = ImageFont.truetype(str(resource_path("TrajanPro-Regular.ttf")), fontsize)
    except Exception as e:
        font = ImageFont.load_default()
    dummy = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    img = Image.new("RGBA", (tw + 10, th + 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), text, font=font, fill=color)
    img = img.rotate(270, expand=True)
    return ImageTk.PhotoImage(img)

def update_vertical_labels(theme):
    global old_label_img, new_label_img, main_menu_img, theme_label_img
    fg = theme["label_fg"]
    old_label_img = make_vertical_label("ORIGINAL TEXTURE", fg, 18)
    new_label_img = make_vertical_label("REPLACED TEXTURE", fg, 18)
    main_menu_img = make_vertical_label("MAIN MENU", fg, 18)
    theme_text = "DARK THEME" if current_theme == DARK else "LIGHT THEME"
    theme_label_img = make_vertical_label(theme_text, fg, 18)
    old_label_canvas.delete("all")
    old_label_canvas.config(bg=theme["bg"], width=old_label_img.width(), height=PREVIEW_SIZE)
    old_label_canvas.create_image(old_label_img.width()//2, PREVIEW_SIZE//2, anchor="center", image=old_label_img)
    new_label_canvas.delete("all")
    new_label_canvas.config(bg=theme["bg"], width=new_label_img.width(), height=PREVIEW_SIZE)
    new_label_canvas.create_image(new_label_img.width()//2, PREVIEW_SIZE//2, anchor="center", image=new_label_img)
    main_menu_canvas.delete("all")
    main_menu_canvas.config(bg=theme["bg"], width=main_menu_img.width(), height=260)
    main_menu_canvas.create_image(main_menu_img.width()//2, 130, anchor="center", image=main_menu_img)
    theme_label_canvas.delete("all")
    theme_label_canvas.config(bg=theme["bg"], width=theme_label_img.width(), height=200)
    theme_label_canvas.create_image(theme_label_img.width()//2, 100, anchor="center", image=theme_label_img)

def update_side_image(theme):
    global side_img_ref
    img_path = resource_path(theme["watermark"])
    if not img_path.exists():
        return
    img = Image.open(img_path).convert("RGBA")
    img.thumbnail((160, 200), Image.LANCZOS)
    side_img_ref = ImageTk.PhotoImage(img)
    side_canvas.delete("all")
    side_canvas.create_image(80, 100, anchor="center", image=side_img_ref)
    side_canvas.config(bg=theme["bg"])

def apply_theme(theme):
    root.config(bg=theme["bg"])
    update_side_image(theme)
    update_vertical_labels(theme)
    sidebar_frame.config(bg=theme["sidebar_bg"])
    sidebar_title.config(bg=theme["sidebar_bg"], fg=theme["fg"])
    sidebar_list_frame.config(bg=theme["sidebar_bg"])
    sidebar_btn_frame.config(bg=theme["sidebar_bg"])
    for widget, kind in all_widgets:
        try:
            if kind == "label":
                widget.config(bg=theme["bg"], fg=theme["fg"])
            elif kind == "label_secondary":
                widget.config(bg=theme["bg"], fg=theme["secondary_fg"])
            elif kind == "label_frame":
                widget.config(bg=theme["frame_bg"], fg=theme["secondary_fg"])
            elif kind == "label_footer":
                widget.config(bg=theme["footer_bg"], fg=theme["secondary_fg"])
            elif kind == "entry":
                widget.config(bg=theme["entry_bg"], fg=theme["entry_fg"], disabledbackground=theme["entry_bg"], disabledforeground=theme["entry_fg"], highlightbackground=theme["border"], highlightcolor=theme["accent"], readonlybackground=theme["entry_bg"])
            elif kind == "frame":
                widget.config(bg=theme["bg"])
            elif kind == "frame_card":
                widget.config(bg=theme["frame_bg"])
            elif kind == "frame_footer":
                widget.config(bg=theme["footer_bg"])
            elif kind == "canvas":
                widget.config(bg=theme["canvas_bg"])
            elif kind == "side_canvas":
                widget.config(bg=theme["bg"])
            elif kind == "vert_canvas":
                widget.config(bg=theme["bg"])
            elif kind == "divider":
                widget.config(bg=theme["border"])
            elif kind == "pointer":
                widget.config(bg=theme["bg"])
            elif kind == "rounded_btn_card":
                update_rounded_button_bg(widget, theme["frame_bg"])
            elif kind == "rounded_btn_bg":
                update_rounded_button_bg(widget, theme["bg"])
            elif kind == "rounded_btn_footer":
                update_rounded_button_bg(widget, theme["footer_bg"])
            elif kind == "rounded_btn_navy":
                update_rounded_button_bg(widget, NAVY)
            elif kind == "label_footer_text":
                widget.config(bg=theme["footer_bg"], fg=theme["secondary_fg"])
            elif kind == "button_footer":
                widget.config(bg=theme["footer_bg"], fg=theme["accent"], activebackground=theme["footer_bg"], activeforeground=NAVY_DARK)
        except:
            pass
    refresh_sidebar()

def reset_all():
    global old_img_ref, new_img_ref, old_img_full, new_img_full
    old_png_path.set("")
    new_png_path.set("")
    output_folder_path.set("")
    old_img_ref = None
    new_img_ref = None
    old_img_full = None
    new_img_full = None
    old_canvas.delete("all")
    old_canvas.config(width=PREVIEW_SIZE, height=PREVIEW_SIZE)
    old_canvas.unbind("<Button-3>")
    new_canvas.delete("all")
    new_canvas.config(width=PREVIEW_SIZE, height=PREVIEW_SIZE)
    new_canvas.unbind("<Button-3>")
    old_info.config(text="")
    new_info.config(text="")
    category_frame.grid_remove()
    sub_category_frame.grid_remove()
    selected_category.set("")
    selected_sub_category.set("")
    category_menu["values"] = []
    sub_category_menu["values"] = []
    new_cat_entry.delete(0, tk.END)
    new_cat_entry.grid_remove()
    confirm_cat_btn.grid_remove()
    cat_sub_frame.grid_remove()

def toggle_theme():
    global current_theme
    if current_theme == LIGHT:
        current_theme = DARK
        draw_topbar_btn(theme_btn_canvas, "☀")
    else:
        current_theme = LIGHT
        draw_topbar_btn(theme_btn_canvas, "🌙")
    apply_theme(current_theme)

def draw_topbar_btn(c, text):
    c.delete("all")
    c.create_text(20, 20, text=text, fill="#ffffff", font=("Segoe UI", 13))
    c.config(bg=NAVY)

def load_preview(path, canvas, label_info):
    global old_img_ref, new_img_ref, old_img_full, new_img_full
    if not path.lower().endswith('.png'):
        messagebox.showerror("Error", "Please select a PNG file.")
        return
    img = Image.open(path).convert("RGBA")
    size_kb = Path(path).stat().st_size / 1024
    orig_w, orig_h = img.size
    ratio = orig_w / orig_h
    if ratio >= 1:
        new_w = PREVIEW_SIZE
        new_h = int(PREVIEW_SIZE / ratio)
    else:
        new_h = PREVIEW_SIZE
        new_w = int(PREVIEW_SIZE * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    canvas.config(width=new_w, height=new_h)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=photo)
    if canvas == old_canvas:
        old_img_ref = photo
        old_img_full = path
        old_png_path.set(path)
        old_canvas.bind("<Button-3>", lambda e: canvas_context_menu(e, "old"))
    else:
        new_img_ref = photo
        new_img_full = path
        new_png_path.set(path)
        new_canvas.bind("<Button-3>", lambda e: canvas_context_menu(e, "new"))
    label_info.config(text=f"{orig_w}x{orig_h}px  |  {size_kb:.1f} KB")

def browse_old():
    path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if path:
        if path == new_png_path.get():
            messagebox.showerror("Error", "The original file is the same as the replacement. Please select a different file.")
            return
        load_preview(path, old_canvas, old_info)

def browse_new():
    path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if path:
        if path == old_png_path.get():
            messagebox.showerror("Error", "The replacement file is the same as the original. Please select a different file.")
            return
        load_preview(path, new_canvas, new_info)

def browse_output():
    path = filedialog.askopenfilename(filetypes=[("INI files", "*.ini")])
    if path:
        output_folder_path.set(path)
        load_categories(path)
        cat_sub_frame.grid()
        category_frame.grid()

def run_replacement():
    old = Path(old_png_path.get())
    new = Path(new_png_path.get())
    out = Path(output_folder_path.get())
    if not old.is_file():
        messagebox.showerror("Error", "Please select the original texture file.")
        return
    if not new.is_file():
        messagebox.showerror("Error", "Please select the new texture file.")
        return
    if not out.is_file():
        messagebox.showerror("Error", "Please select a valid textures.ini file.")
        return
    if old_png_path.get() == new_png_path.get():
        messagebox.showerror("Error", "The original and replacement files are the same. Please select a different file.")
        return
    original_stem = old.stem
    last_8 = original_stem[-8:]
    ini_key = "0000000000000000" + last_8
    ini_root = Path(output_folder_path.get()).parent
    try:
        ini_value = new.relative_to(ini_root).as_posix()
    except ValueError:
        ini_value = new.parent.name + "/" + new.name
    log_path = out
    category = selected_category.get()
    if category == "No Category":
        header = None
        parent_header = None
    elif category == "New Category...":
        category = new_cat_entry.get().strip()
        if not category:
            messagebox.showerror("Error", "Please enter a category name.")
            return
        sub = selected_sub_category.get()
        header = f">{category}"
        parent_header = None
    else:
        sub = selected_sub_category.get()
        if sub:
            header = f">>{sub}"
            parent_header = f">{category}"
        else:
            header = f">{category}"
            parent_header = None
    orig_img = Image.open(old)
    repl_img = Image.open(new)
    orig_ratio = orig_img.width / orig_img.height
    repl_ratio = repl_img.width / repl_img.height
    if abs(orig_ratio - repl_ratio) > 0.01:
        proceed = messagebox.askyesno("Aspect Ratio Mismatch",
            f"The original texture is {orig_img.width}x{orig_img.height} and the replacement is {repl_img.width}x{repl_img.height}.\n\nThe aspect ratios don't match. This will cause visual glitches in-game.\n\nDo you want to proceed anyway?")
        if not proceed:
            return
    with open(log_path, "r") as f:
        existing_lines = f.readlines()
    for line in existing_lines:
        if ini_key in line:
            messagebox.showwarning("Already exists!", f"An entry with the key '{last_8}' already exists in textures.ini.\n\nNo changes were made.")
            return

    replacement_name = new.name.lower()
    for line in existing_lines:
        if "=" in line and not line.strip().startswith(">"):
            existing_file = line.split("=", 1)[1].strip()
            if Path(existing_file).name.lower() == replacement_name:
                messagebox.showwarning(
                    "Duplicate Filename",
                    f'A file named "{new.name}" is already referenced in textures.ini.\n\n'
                    f'Please rename your replacement texture before appending.'
                )
                return

    with open(log_path, "r") as f:
        content = f.read()
    lines = content.split("\n")
    if header is None:
        with open(log_path, "a") as f:
            f.write(f"\n{ini_key} = {ini_value}")
        messagebox.showinfo("Done!", f"Entry added successfully!\n\nDon't forget to check 'Replace textures' in:\nSettings > Tools > Developer tools > Texture replacement > Replace textures")
        return
    header_found = any(line.strip() == header for line in lines)
    parent_found = any(line.strip() == parent_header for line in lines) if parent_header else False
    if header_found:
        new_lines = []
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped == header:
                new_lines.append(lines[i])
                i += 1
                section_entries = []
                while i < len(lines):
                    s = lines[i].strip()
                    if s.startswith(">") or s == "":
                        break
                    section_entries.append(lines[i].rstrip("\n"))
                    i += 1
                section_entries.append(f"{ini_key} = {ini_value}")
                section_entries.sort(key=lambda x: Path(x.split("=")[1].strip()).name.lower() if "=" in x else "")
                for entry in section_entries:
                    new_lines.append(entry + "\n")
                continue
            new_lines.append(lines[i])
            i += 1
        with open(log_path, "w") as f:
            f.writelines(new_lines)
    elif parent_found:
        new_lines = []
        i = 0
        inserted = False
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped == parent_header and not inserted:
                new_lines.append(lines[i])
                i += 1
                sub_name = header.lstrip(">").lower()
                pending = []
                while i < len(lines):
                    s = lines[i].strip()
                    if s.startswith(">") and not s.startswith(">>"):
                        break
                    pending.append(lines[i])
                    i += 1
                insert_pos = len(pending)
                for j, pline in enumerate(pending):
                    ps = pline.strip()
                    if ps.startswith(">>"):
                        existing_sub = ps.lstrip(">").lower()
                        if sub_name < existing_sub:
                            insert_pos = j
                            break
                pending.insert(insert_pos, f"{ini_key} = {ini_value}\n")
                pending.insert(insert_pos, f"{header}\n")
                new_lines.extend(pending)
                inserted = True
                continue
            new_lines.append(lines[i])
            i += 1
        with open(log_path, "w") as f:
            f.writelines(new_lines)
    else:
        new_block_lines = []
        if parent_header:
            new_block_lines = [f"{parent_header}\n", f"{header}\n", f"{ini_key} = {ini_value}\n"]
        else:
            new_block_lines = [f"{header}\n", f"{ini_key} = {ini_value}\n"]
        cat_name = (parent_header or header).lstrip(">").lower()
        insert_at = len(lines)
        for i, line in enumerate(lines):
            s = line.strip()
            if s.startswith(">") and not s.startswith(">>"):
                if cat_name < s.lstrip(">").lower():
                    insert_at = i
                    break
        new_block_lines.insert(0, "\n")
        for j, bl in enumerate(new_block_lines):
            lines.insert(insert_at + j, bl)
        with open(log_path, "w") as f:
            f.write("".join(lines))
            
    messagebox.showinfo("Done!", f"Entry added successfully!\n\nDon't forget to check 'Replace textures' in:\nSettings > Tools > Developer tools > Texture replacement > Replace textures")

def open_discord():
    webbrowser.open(DISCORD_URL)

CHANGELOG = {
    "v1.0.3": [
        "After testing with other games, app has been renamed to 'PPSSPP Texture Replacement Tool'",
        "Changed category and sub-category prefix from '#' to '>' to avoid conflicts with INI comment syntax.",
        "Added 'Edit' button next to Category and Sub-Category dropdowns: allows adding sub-categories, renaming, and deleting directly from the UI.",
        "Added a '✓' confirm button when adding a New Category.",
        "Fonts embedded to package.",
        "Changed body fonts and some capitalization.",
        "Fixed aspect ratio warning not showing: User now has a prompt to choose whether to proceed or go back before appending.",
        "Preview frames are now centered: If the image was too thin, the Original Texture frame was anchored to the top while Replaced Texture was centered. Both are now centered.",
        "Added 'Show in Explorer' function: A folder icon appears on both directory blocks once a PNG is selected, opening the containing folder and highlighting the file.",
        "Added current version label next to title: Clicking it shows the Changelog.",
        "Fixed filename duplicate warning: Previously only triggered if the hex filename was already in textures.ini. Now also checks the Replaced Texture's filename.",
        "[macOS] Larger overall GUI text.",
        "[macOS] Removed context menu when right-clicking empty preview frames.",
        "[macOS] Fixed Applications alias in installation disk image.",
    ],
    "v1.0.2": [
        "Fixed crash when textures.ini is empty.",
        "Improved aspect ratio warning message.",
        "Minor UI adjustments.",
        "Added pointer animation to append button.",
        "Added macOS support.",
    ],
    "v1.0.1": [
        "Initial release of 'Dissidia 012 Texture Replacement Tool'.",
    ],
}

def show_changelog():
    popup = tk.Toplevel(root)
    popup.title("Version Changelog")
    popup.config(bg=current_theme["bg"])
    popup.resizable(False, False)
    popup.grab_set()
    popup.iconbitmap(str(resource_path("chocobo2.ico")))

    tk.Label(popup, text="Changelog", font=FONT_TITLE, bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=(16, 8), padx=24)

    frame = tk.Frame(popup, bg=current_theme["bg"])
    frame.pack(padx=24, pady=(0, 16), fill="both", expand=True)

    for version, notes in CHANGELOG.items():
        tk.Label(frame, text=version, font=FONT_TITLE2, bg=current_theme["bg"], fg=current_theme["fg"], anchor="w").pack(fill="x", pady=(8, 2))
        for note in notes:
            tk.Label(frame, text=f"  • {note}", font=FONT_BODY, bg=current_theme["bg"], fg=current_theme["secondary_fg"], anchor="w", justify="left").pack(fill="x")

root.columnconfigure(0, weight=0, minsize=140)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=0)
root.rowconfigure(4, weight=1)

# --- Top bar ---
top_frame = tk.Frame(root, bg=NAVY)
top_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
top_frame.columnconfigure(0, weight=1)

title_frame = tk.Frame(top_frame, bg=NAVY)
title_frame.grid(row=0, column=0, sticky="w")

lbl_title = tk.Label(title_frame, text="PPSSPP Texture Replacement Tool", font=FONT_TITLE, bg=NAVY, fg="#ffffff", pady=14, padx=16)
lbl_title.grid(row=0, column=0, sticky="w")

lbl_version = tk.Label(title_frame, text="v1.0.3", font=FONT_FOOTER, bg=NAVY, fg="#ffffff", padx=0, pady=14)
lbl_version.grid(row=0, column=1, sticky="w")
lbl_version.config(cursor="hand2")
lbl_version.bind("<Button-1>", lambda e: show_changelog())

banner_img_raw = Image.open(resource_path("banner.png")).convert("RGBA")
banner_img_raw.thumbnail((200, 40), Image.LANCZOS)
banner_img_ref = ImageTk.PhotoImage(banner_img_raw)
banner_label = tk.Label(top_frame, image=banner_img_ref, bg=NAVY)
banner_label.image = banner_img_ref
banner_label.grid(row=0, column=1, sticky="e", padx=8)

reset_btn_canvas = tk.Canvas(top_frame, width=40, height=40, highlightthickness=0, bg=NAVY, cursor="hand2")
reset_btn_canvas.grid(row=0, column=2, sticky="e", padx=0)
reset_btn_canvas.create_text(20, 20, text="↺", fill="#ffffff", font=("Segoe UI", 13))
reset_btn_canvas.bind("<Button-1>", lambda e: reset_all())
reset_btn_canvas.bind("<Enter>", lambda e: reset_btn_canvas.config(bg=NAVY_DARK))
reset_btn_canvas.bind("<Leave>", lambda e: reset_btn_canvas.config(bg=NAVY))
all_widgets.append((reset_btn_canvas, "rounded_btn_navy"))

theme_btn_canvas = tk.Canvas(top_frame, width=40, height=40, highlightthickness=0, bg=NAVY, cursor="hand2")
theme_btn_canvas.grid(row=0, column=3, sticky="e", padx=8)
theme_btn_canvas.create_text(20, 20, text="☀", fill="#ffffff", font=("Segoe UI", 13))
theme_btn_canvas.bind("<Button-1>", lambda e: toggle_theme())
theme_btn_canvas.bind("<Enter>", lambda e: theme_btn_canvas.config(bg=NAVY_DARK))
theme_btn_canvas.bind("<Leave>", lambda e: theme_btn_canvas.config(bg=NAVY))
all_widgets.append((theme_btn_canvas, "rounded_btn_navy"))

# --- Sidebar ---
sidebar_frame = tk.Frame(root, width=220, height=600, bg=DARK["sidebar_bg"])
sidebar_frame.grid(row=1, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_propagate(False)

sidebar_title = tk.Label(sidebar_frame, text="games", font=FONT_TITLE2, bg=DARK["sidebar_bg"], fg=DARK["fg"], pady=8, padx=8, anchor="center")
sidebar_title.pack(fill="x")

sidebar_list_frame = tk.Frame(sidebar_frame, bg=DARK["sidebar_bg"])
sidebar_list_frame.place(x=0, y=30, relwidth=1, rely=0, relheight=1, height=-64)

def sidebar_right_click(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="+ Add Game Folder", command=add_game_to_history)
    menu.add_separator()
    sort_menu = tk.Menu(menu, tearoff=0)
    sort_menu.add_command(label="Alphabetically (A-Z)", command=lambda: sort_history("alpha_asc"))
    sort_menu.add_command(label="Alphabetically (Z-A)", command=lambda: sort_history("alpha_desc"))
    sort_menu.add_command(label="Last Added", command=lambda: sort_history("last_added"))
    sort_menu.add_command(label="Recent", command=lambda: sort_history("recent"))
    menu.add_cascade(label="Sort by", menu=sort_menu)
    menu.tk_popup(event.x_root, event.y_root)

sidebar_list_frame.bind("<Button-3>", sidebar_right_click)
sidebar_title.bind("<Button-3>", sidebar_right_click)

sidebar_btn_frame = tk.Frame(root, bg=DARK["sidebar_bg"])
sidebar_btn_frame.grid(row=4, column=0, sticky="ew")

add_game_btn = tk.Button(sidebar_btn_frame, text="+ Add Game Folder", command=add_game_to_history, font=FONT_SMALL, bg=NAVY, fg="#ffffff", relief="flat", cursor="hand2", pady=6, borderwidth=0)
add_game_btn.pack(fill="x", padx=4, pady=4)

# --- Far left vertical labels ---
main_menu_canvas = tk.Canvas(root, highlightthickness=0, width=30, height=260)
main_menu_canvas.grid(row=1, column=1, sticky="ns", padx=(8, 0), pady=(16, 0))
all_widgets.append((main_menu_canvas, "vert_canvas"))

theme_label_canvas = tk.Canvas(root, highlightthickness=0, width=30, height=200)
theme_label_canvas.grid(row=2, column=1, sticky="", padx=(8, 0), pady=(40, 16))
all_widgets.append((theme_label_canvas, "vert_canvas"))

def open_ini_file():
    path = output_folder_path.get()
    if path and Path(path).is_file():
        import os
        os.startfile(path)
    else:
        messagebox.showerror("Error", "Please select a textures.ini file first.")

def open_in_explorer(path):
    if path and Path(path).is_file():
        import subprocess
        windows_path = str(Path(path).resolve())
        subprocess.Popen(f'explorer /select,"{windows_path}"', shell=True)
    else:
        messagebox.showerror("Error", "Please select a file first.")

def show_edit_menu_cat(event=None):
    cat = selected_category.get()
    if not cat or cat in ("No Category", "New Category..."):
        messagebox.showerror("Error", "Please select a valid category first.")
        return
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Add Sub-Category", command=add_sub_category)
    menu.add_command(label="Rename", command=lambda: rename_category(cat))
    menu.add_command(label="Delete", command=lambda: delete_category(cat))
    x = add_sub_btn_cat.winfo_rootx()
    y = add_sub_btn_cat.winfo_rooty() + add_sub_btn_cat.winfo_height()
    menu.tk_popup(x, y)

def show_edit_menu_sub(event=None):
    sub = selected_sub_category.get()
    cat = selected_category.get()
    if not sub:
        messagebox.showerror("Error", "Please select a valid sub-category first.")
        return
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Add Sub-Category", command=add_sub_category)
    menu.add_command(label="Rename", command=lambda: rename_sub_category(cat, sub))
    menu.add_command(label="Delete", command=lambda: delete_sub_category(cat, sub))
    x = add_sub_btn.winfo_rootx()
    y = add_sub_btn.winfo_rooty() + add_sub_btn.winfo_height()
    menu.tk_popup(x, y)

def rename_category(cat):
    new_name = ask_string_borderless("Rename Category", f"Enter new name for '{cat}':")
    if not new_name:
        return
    import re
    if not re.match(r'^[a-zA-Z0-9_\-]+$', new_name):
        messagebox.showerror("Error", "Name can only contain letters, numbers, underscores and hyphens.")
        return
    ini_path = output_folder_path.get()
    if not ini_path or not Path(ini_path).is_file():
        return
    with open(ini_path, "r") as f:
        content = f.read()
    content = content.replace(f">{cat}\n", f">{new_name}\n")
    with open(ini_path, "w") as f:
        f.write(content)
    load_categories(ini_path)

def delete_category(cat):
    if not messagebox.askyesno("Delete Category", f"Delete category '{cat}'?\n\nEntries inside will NOT be deleted."):
        return
    ini_path = output_folder_path.get()
    if not ini_path or not Path(ini_path).is_file():
        return
    with open(ini_path, "r") as f:
        lines = f.readlines()
    with open(ini_path, "w") as f:
        for line in lines:
            if line.strip() != f">{cat}":
                f.write(line)
    load_categories(ini_path)

def rename_sub_category(cat, sub):
    new_name = ask_string_borderless("Rename Sub-Category", f"Enter new name for '{sub}':")
    if not new_name:
        return
    import re
    if not re.match(r'^[a-zA-Z0-9_\-]+$', new_name):
        messagebox.showerror("Error", "Name can only contain letters, numbers, underscores and hyphens.")
        return
    ini_path = output_folder_path.get()
    if not ini_path or not Path(ini_path).is_file():
        return
    with open(ini_path, "r") as f:
        content = f.read()
    content = content.replace(f">>{sub}\n", f">>{new_name}\n")
    with open(ini_path, "w") as f:
        f.write(content)
    load_categories(ini_path)

def delete_sub_category(cat, sub):
    if not messagebox.askyesno("Delete Sub-Category", f"Delete sub-category '{sub}'?\n\nEntries inside will NOT be deleted."):
        return
    ini_path = output_folder_path.get()
    if not ini_path or not Path(ini_path).is_file():
        return
    with open(ini_path, "r") as f:
        lines = f.readlines()
    with open(ini_path, "w") as f:
        for line in lines:
            if line.strip() != f">>{sub}":
                f.write(line)
    load_categories(ini_path)

def add_sub_category():
    cat = selected_category.get()
    if not cat or cat == "No Category" or cat == "New Category...":
        messagebox.showerror("Error", "Please select a valid category first.")
        return
    new_sub = ask_string_borderless("Add Sub-Category", f"Enter new sub-category name under '{cat}':")
    if not new_sub:
        return
    import re
    if not re.match(r'^[a-zA-Z0-9_\-]+$', new_sub):
        messagebox.showerror("Error", "Sub-category name can only contain letters, numbers, underscores and hyphens. No spaces or special characters allowed.")
        return
    sub_map = getattr(category_menu, '_sub_map', {})
    subs = sub_map.get(cat, [])
    if new_sub in subs:
        messagebox.showwarning("Already exists", f"'{new_sub}' already exists under '{cat}'.")
        return
    subs.append(new_sub)
    subs.sort()
    sub_map[cat] = subs
    category_menu._sub_map = sub_map
    sub_category_menu["values"] = subs
    selected_sub_category.set(new_sub)
    sub_category_frame.grid()
    add_sub_btn_cat.grid()

    ini_path = output_folder_path.get()
    if ini_path and Path(ini_path).is_file():
        with open(ini_path, "r") as f:
            lines = f.readlines()
        final_lines = []
        in_cat = False
        existing_subs = []
        cat_line_idx = None
        for i, line in enumerate(lines):
            if line.strip() == f">{cat}":
                in_cat = True
                cat_line_idx = i
                final_lines.append(line)
            elif in_cat and line.strip().startswith(">>"):
                existing_subs.append(line.strip()[2:])
            elif in_cat:
                existing_subs.append(new_sub)
                existing_subs = sorted(set(existing_subs))
                for s in existing_subs:
                    final_lines.append(f">>{s}\n")
                in_cat = False
                existing_subs = []
                final_lines.append(line)
            else:
                final_lines.append(line)
        if in_cat:
            existing_subs.append(new_sub)
            existing_subs = sorted(set(existing_subs))
            for s in existing_subs:
                final_lines.append(f">>{s}\n")
        with open(ini_path, "w") as f:
            f.writelines(final_lines)

# --- Main card ---
card = tk.Frame(root, padx=20, pady=8, height=280)
card.grid(row=1, column=2, sticky="new", padx=16, pady=(16, 0))
card.columnconfigure(0, weight=1)
card.columnconfigure(1, minsize=32)
card.columnconfigure(2, minsize=80)
card.grid_propagate(False)
all_widgets.append((card, "frame_card"))

def add_field(parent, label_text, var, browse_cmd, row, clear_cmd=None, extra_cmd=None, extra_icon="👁"):
    lbl = tk.Label(parent, text=label_text, font=FONT_HEADER, anchor="w")
    lbl.grid(row=row, column=0, columnspan=3, sticky="w", pady=(4, 2))
    all_widgets.append((lbl, "label_frame"))
    entry_frame = tk.Frame(parent, bg=current_theme["frame_bg"])
    entry_frame.grid(row=row+1, column=0, sticky="ew", padx=(0, 4))
    entry_frame.columnconfigure(0, weight=1)
    all_widgets.append((entry_frame, "frame_card"))
    ent = tk.Entry(entry_frame, textvariable=var, state="readonly", font=FONT_BODY, relief="flat", highlightthickness=1)
    ent.grid(row=0, column=0, sticky="ew", ipady=7)
    all_widgets.append((ent, "entry"))
    eye_lbl = tk.Label(entry_frame, text=extra_icon, font=("Segoe UI", 10), bg=current_theme["frame_bg"], fg=current_theme["secondary_fg"], cursor="hand2", padx=4)
    if extra_cmd:
        eye_lbl.grid(row=0, column=1, sticky="e")
        eye_lbl.grid_remove()
        eye_lbl.bind("<Button-1>", lambda e: extra_cmd())
    all_widgets.append((eye_lbl, "label_frame"))
    ent.config(highlightthickness=0)
    entry_frame.config(highlightthickness=1, highlightbackground=current_theme["border"])
    all_widgets.append((eye_lbl, "label_frame"))
    x_c = make_rounded_button(parent, "✕", clear_cmd, font=("Segoe UI", 8), width=28, height=28, bg=NAVY, fg="#ffffff", hover_bg=NAVY_DARK, parent_bg=current_theme["frame_bg"])
    x_c.grid(row=row+1, column=1, padx=(0, 4))
    x_c.grid_remove()
    all_widgets.append((x_c, "rounded_btn_card"))
    br_c = make_rounded_button(parent, "Browse", browse_cmd, font=FONT_BUTTON, width=80, height=32, bg=NAVY, fg="#ffffff", hover_bg=NAVY_DARK, parent_bg=current_theme["frame_bg"])
    br_c.grid(row=row+1, column=2, sticky="e")
    all_widgets.append((br_c, "rounded_btn_card"))
    def on_var_change(*args):
        if var.get():
            x_c.grid()
            if extra_cmd:
                eye_lbl.grid()
        else:
            x_c.grid_remove()
            if extra_cmd:
                eye_lbl.grid_remove()
    var.trace_add("write", on_var_change)

add_field(card, "Original Texture PNG File", old_png_path, browse_old, 0, lambda: clear_old(), extra_cmd=lambda: open_in_explorer(old_png_path.get()), extra_icon="👁")
add_field(card, "Replacement Texture PNG File", new_png_path, browse_new, 2, lambda: clear_new(), extra_cmd=lambda: open_in_explorer(new_png_path.get()), extra_icon="👁")
add_field(card, "textures.ini File", output_folder_path, browse_output, 4, lambda: clear_output(), extra_cmd=open_ini_file, extra_icon="👁")

cat_sub_frame = tk.Frame(card)
cat_sub_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(10, 2))
cat_sub_frame.columnconfigure(0, weight=1, uniform="equal")
cat_sub_frame.columnconfigure(1, weight=1, uniform="equal")
all_widgets.append((cat_sub_frame, "frame_card"))

category_frame = tk.Frame(cat_sub_frame)
category_frame.grid(row=0, column=0, sticky="ew", padx=(0, 4))
category_frame.columnconfigure(0, weight=1)
all_widgets.append((category_frame, "frame_card"))

cat_lbl = tk.Label(category_frame, text="Category", font=FONT_HEADER, anchor="w")
cat_lbl.grid(row=0, column=0, sticky="w", pady=(0, 2))
all_widgets.append((cat_lbl, "label_frame"))

category_menu = ttk.Combobox(category_frame, textvariable=selected_category, state="readonly", font=FONT_BODY)
category_menu.grid(row=1, column=0, sticky="ew", padx=(0, 4), ipady=4)

add_sub_btn_cat = make_rounded_button(category_frame, "🖉", show_edit_menu_cat, font=("Segoe UI", 11), width=28, height=28, bg=NAVY, fg="#ffffff", hover_bg=NAVY_DARK, parent_bg=current_theme["frame_bg"])
add_sub_btn_cat.grid(row=1, column=1, sticky="e")
all_widgets.append((add_sub_btn_cat, "rounded_btn_card"))
category_frame.columnconfigure(1, minsize=32)
add_sub_btn_cat.grid_remove()

sub_category_frame = tk.Frame(cat_sub_frame)
sub_category_frame.grid(row=0, column=1, sticky="ew", padx=(4, 0))
sub_category_frame.columnconfigure(0, weight=1)
all_widgets.append((sub_category_frame, "frame_card"))

sub_lbl = tk.Label(sub_category_frame, text="Sub-Category", font=FONT_HEADER, anchor="w")
sub_lbl.grid(row=0, column=0, sticky="w", pady=(0, 2))
all_widgets.append((sub_lbl, "label_frame"))

sub_category_menu = ttk.Combobox(sub_category_frame, textvariable=selected_sub_category, state="readonly", font=FONT_BODY)
sub_category_menu.grid(row=1, column=0, sticky="ew", ipady=4, padx=(0, 4))

add_sub_btn = make_rounded_button(sub_category_frame, "🖉", show_edit_menu_sub, font=("Segoe UI", 11), width=28, height=28, bg=NAVY, fg="#ffffff", hover_bg=NAVY_DARK, parent_bg=current_theme["frame_bg"])
add_sub_btn.grid(row=1, column=1, sticky="e")
all_widgets.append((add_sub_btn, "rounded_btn_card"))
sub_category_frame.columnconfigure(1, minsize=32)

new_cat_frame = tk.Frame(cat_sub_frame)
new_cat_frame.grid(row=0, column=1, sticky="ew", padx=(4, 0))
new_cat_frame.columnconfigure(0, weight=1)
all_widgets.append((new_cat_frame, "frame_card"))

name_lbl = tk.Label(new_cat_frame, text="Name:", font=FONT_HEADER, anchor="w")
name_lbl.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 2))
all_widgets.append((name_lbl, "label_frame"))

new_cat_entry = tk.Entry(new_cat_frame, font=FONT_BODY, relief="flat", highlightthickness=2)
new_cat_entry.grid(row=1, column=0, sticky="ew", padx=(0, 2), ipady=4)
all_widgets.append((new_cat_entry, "entry"))

# Tooltip
tooltip_win = None
def show_tooltip(event):
    global tooltip_win
    tooltip_win = tk.Toplevel(root)
    tooltip_win.wm_overrideredirect(True)
    tooltip_win.wm_geometry(f"+{event.x_root + 12}+{event.y_root + 16}")
    tk.Label(tooltip_win, text="No spaces or special characters.\nUse letters, numbers, _ or -", font=FONT_SMALL,
             bg="#ffffe0", fg="#333333", relief="solid", borderwidth=1, padx=6, pady=4).pack()
def hide_tooltip(event):
    global tooltip_win
    if tooltip_win:
        tooltip_win.destroy()
        tooltip_win = None
new_cat_entry.bind("<Enter>", show_tooltip)
new_cat_entry.bind("<Leave>", hide_tooltip)
new_cat_entry.bind("<FocusOut>", hide_tooltip)

def confirm_new_category():
    import re
    cat = new_cat_entry.get().strip()
    if not cat:
        messagebox.showerror("Error", "Please enter a category name.")
        return
    if not re.match(r'^[a-zA-Z0-9_\-]+$', cat):
        messagebox.showerror("Error", "Category name can only contain letters, numbers, underscores and hyphens.\nNo spaces or special characters allowed.")
        return
    ini_path = output_folder_path.get()
    if not ini_path or not Path(ini_path).is_file():
        messagebox.showerror("Error", "Please select a textures.ini file first.")
        return
    with open(ini_path, "r") as f:
        content = f.read()
    header = f">{cat}"
    if header in content.split("\n"):
        messagebox.showwarning("Already exists", f"Category '{cat}' already exists in textures.ini.")
        return
    with open(ini_path, "a") as f:
        f.write(f"\n{header}\n")
    load_categories(ini_path)
    # Select the newly added category
    vals = list(category_menu["values"])
    if cat in vals:
        selected_category.set(cat)
        on_category_change()
    messagebox.showinfo("Done!", f"Category '{cat}' added to textures.ini.")

confirm_cat_btn = make_rounded_button(new_cat_frame, "✓", confirm_new_category, font=("Segoe UI", 9, "bold"), width=28, height=28, bg="#2e7d32", fg="#ffffff", hover_bg="#1b5e20", parent_bg=current_theme["frame_bg"])
confirm_cat_btn.grid(row=1, column=1, padx=(0, 2))
all_widgets.append((confirm_cat_btn, "rounded_btn_card"))

new_cat_entry.grid_remove()
confirm_cat_btn.grid_remove()
new_cat_frame.grid_remove()

category_menu.bind("<<ComboboxSelected>>", lambda e: (on_category_change(), root.update()))
sub_category_menu.bind("<<ComboboxSelected>>", lambda e: root.update())
category_frame.grid_remove()
sub_category_frame.grid_remove()
cat_sub_frame.grid_remove()

# --- Bottom ---
bottom_frame = tk.Frame(root)
bottom_frame.grid(row=2, column=2, sticky="ew", padx=16, pady=(8, 4))
bottom_frame.columnconfigure(0, weight=0)
bottom_frame.columnconfigure(1, weight=1)
bottom_frame.columnconfigure(2, weight=0)
all_widgets.append((bottom_frame, "frame"))

side_canvas = tk.Canvas(bottom_frame, width=160, height=200, highlightthickness=0)
side_canvas.grid(row=0, column=0, sticky="w", padx=(0, 16))
all_widgets.append((side_canvas, "side_canvas"))
side_canvas.bind("<Button-1>", lambda e: toggle_theme())
side_canvas.config(cursor="hand2")

pointer_img_raw = Image.open(resource_path("pointer.png")).convert("RGBA")
pointer_img_raw = pointer_img_raw.resize((36, 28), Image.LANCZOS)
pointer_img_ref = ImageTk.PhotoImage(pointer_img_raw)

right_frame = tk.Frame(bottom_frame)
right_frame.grid(row=0, column=2, sticky="e")
all_widgets.append((right_frame, "frame"))

pointer_canvas = tk.Canvas(right_frame, width=60, height=28, highlightthickness=0, bg=current_theme["bg"])
pointer_canvas.grid(row=0, column=0, sticky="e")
all_widgets.append((pointer_canvas, "vert_canvas"))

pointer_item = pointer_canvas.create_image(0, 14, anchor="w", image=pointer_img_ref)

def animate_pointer():
    positions = [18, 22]
    def step(i=0):
        pointer_canvas.coords(pointer_item, positions[i], 14)
        root.after(300, step, (i + 1) % len(positions))
    step()

animate_pointer()

def check_fields(*args):
    if old_png_path.get() and new_png_path.get() and output_folder_path.get():
        pointer_canvas.grid()
    else:
        pointer_canvas.grid_remove()

old_png_path.trace_add("write", check_fields)
new_png_path.trace_add("write", check_fields)
output_folder_path.trace_add("write", check_fields)
check_fields()

append_btn = make_rounded_button(right_frame, "Append to textures.ini", run_replacement, font=("Trajan Pro", 10, "bold"), width=220, height=36, bg=NAVY, fg="#ffffff", hover_bg=NAVY_DARK, parent_bg=current_theme["bg"])
append_btn.grid(row=0, column=1, sticky="e")
all_widgets.append((append_btn, "rounded_btn_bg"))

def show_preview_popup(path, title):
    if not path:
        return
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.config(bg=current_theme["bg"])
    popup.resizable(True, True)
    img = Image.open(path).convert("RGBA")
    img.thumbnail((800, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    lbl = tk.Label(popup, image=photo, bg=current_theme["bg"])
    lbl.image = photo
    lbl.pack(padx=16, pady=16)
    popup.grab_set()

def canvas_context_menu(event, canvas_type):
    global old_img_full, new_img_full
    menu = tk.Menu(root, tearoff=0)
    if canvas_type == "old":
        menu.add_command(label="Preview", command=lambda: show_preview_popup(old_img_full, "Original Texture"))
        menu.add_command(label="Replace", command=browse_old)
        menu.add_command(label="Remove", command=clear_old)
    else:
        menu.add_command(label="Preview", command=lambda: show_preview_popup(new_img_full, "Replacement Texture"))
        menu.add_command(label="Replace", command=browse_new)
        menu.add_command(label="Remove", command=clear_new)
    menu.tk_popup(event.x_root, event.y_root)

# --- Previews ---
preview_frame = tk.Frame(root)
preview_frame.grid(row=1, column=3, rowspan=4, padx=(0, 8), pady=(16, 0), sticky="ns")
all_widgets.append((preview_frame, "frame"))

old_canvas = tk.Canvas(preview_frame, width=PREVIEW_SIZE, height=PREVIEW_SIZE, highlightthickness=1, highlightbackground=NAVY)
old_canvas.grid(row=0, column=0, pady=(0, 4))
all_widgets.append((old_canvas, "canvas"))
old_canvas.bind("<Double-Button-1>", lambda e: browse_old())

old_info = tk.Label(preview_frame, text="", font=FONT_SMALL)
old_info.grid(row=1, column=0, pady=(0, 8))
all_widgets.append((old_info, "label_secondary"))

old_label_canvas = tk.Canvas(preview_frame, highlightthickness=0, width=20, height=PREVIEW_SIZE)
old_label_canvas.grid(row=0, column=1, sticky="ns", padx=(4, 0))
all_widgets.append((old_label_canvas, "vert_canvas"))

new_canvas = tk.Canvas(preview_frame, width=PREVIEW_SIZE, height=PREVIEW_SIZE, highlightthickness=1, highlightbackground=NAVY)
new_canvas.grid(row=2, column=0, pady=(0, 4))
all_widgets.append((new_canvas, "canvas"))
new_canvas.bind("<Double-Button-1>", lambda e: browse_new())

new_info = tk.Label(preview_frame, text="", font=FONT_SMALL)
new_info.grid(row=3, column=0, pady=(0, 0))
all_widgets.append((new_info, "label_secondary"))

new_label_canvas = tk.Canvas(preview_frame, highlightthickness=0, width=20, height=PREVIEW_SIZE)
new_label_canvas.grid(row=2, column=1, sticky="ns", padx=(4, 0))
all_widgets.append((new_label_canvas, "vert_canvas"))

def clear_old():
    global old_img_ref, old_img_full
    old_png_path.set("")
    old_img_ref = None
    old_img_full = None
    old_canvas.delete("all")
    old_canvas.config(width=PREVIEW_SIZE, height=PREVIEW_SIZE)
    old_info.config(text="")
    old_canvas.unbind("<Button-3>")

def clear_new():
    global new_img_ref, new_img_full
    new_png_path.set("")
    new_img_ref = None
    new_img_full = None
    new_canvas.delete("all")
    new_canvas.config(width=PREVIEW_SIZE, height=PREVIEW_SIZE)
    new_info.config(text="")
    new_canvas.unbind("<Button-3>")

def clear_output():
    output_folder_path.set("")
    cat_sub_frame.grid_remove()
    category_frame.grid_remove()
    sub_category_frame.grid_remove()
    selected_category.set("")
    selected_sub_category.set("")
    category_menu["values"] = []
    sub_category_menu["values"] = []
    new_cat_entry.delete(0, tk.END)
    new_cat_frame.grid_remove()
    confirm_cat_btn.grid_remove()

# --- Footer ---
footer = tk.Frame(root)
footer.grid(row=5, column=0, columnspan=4, sticky="sew")
footer.columnconfigure(1, weight=1)
all_widgets.append((footer, "frame_footer"))

lbl_credit = tk.Label(footer, text="Created by Link Garcia", font=FONT_FOOTER, pady=10, padx=12)
lbl_credit.grid(row=0, column=0, sticky="w")
all_widgets.append((lbl_credit, "label_footer_text"))

links_frame = tk.Frame(footer)
links_frame.grid(row=0, column=1, sticky="e", padx=10)
all_widgets.append((links_frame, "frame_footer"))

def make_link(parent, text, url, col):
    btn = tk.Button(parent, text=text, command=lambda: webbrowser.open(url), font=FONT_SMALL, relief="flat", cursor="hand2", padx=6, pady=10, borderwidth=0)
    btn.grid(row=0, column=col)
    btn.bind("<Enter>", lambda e, b=btn: b.config(fg="#ffffff" if current_theme == DARK else "#000000"))
    btn.bind("<Leave>", lambda e, b=btn: b.config(fg=NAVY))
    all_widgets.append((btn, "button_footer"))

make_link(links_frame, "🎮 Discord", "https://discord.gg/wbpgtKNSM7", 0)
make_link(links_frame, "🐙 GitHub", "https://github.com/LiinkPK/Dissidia-012-HD-Textures", 1)
make_link(links_frame, "👾 Reddit", "https://www.reddit.com/r/dissidia/comments/1g6peh2/dissidia_012_hd_remastered_wip/", 2)
make_link(links_frame, "🎨 Patreon", "https://www.patreon.com/c/LinkG/membership", 3)
make_link(links_frame, "💙 PayPal", "https://www.paypal.com/paypalme/liinkpk", 4)

def on_category_change():
    cat = selected_category.get()
    if cat == "New Category...":
        sub_category_frame.grid_remove()
        new_cat_frame.grid()
        new_cat_entry.grid()
        confirm_cat_btn.grid()
        add_sub_btn_cat.grid_remove()
        selected_sub_category.set("")
    elif cat == "No Category":
        new_cat_frame.grid_remove()
        new_cat_entry.grid_remove()
        confirm_cat_btn.grid_remove()
        sub_category_frame.grid_remove()
        add_sub_btn_cat.grid_remove()
        selected_sub_category.set("")
    else:
        new_cat_frame.grid_remove()
        new_cat_entry.grid_remove()
        confirm_cat_btn.grid_remove()
        sub_map = getattr(category_menu, '_sub_map', {})
        subs = sub_map.get(cat, [])
        if subs:
            sub_category_menu["values"] = subs
            selected_sub_category.set(subs[0])
            sub_category_frame.grid()
            add_sub_btn_cat.grid()
        else:
            selected_sub_category.set("")
            sub_category_frame.grid_remove()
            add_sub_btn_cat.grid()

def load_categories(path):
    top_level = []
    sub_map = {}
    current_top = None
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(">>"):
                    sub = line[2:].strip()
                    if current_top:
                        sub_map.setdefault(current_top, []).append(sub)
                elif line.startswith(">"):
                    current_top = line[1:].strip()
                    if current_top and current_top not in top_level:
                        top_level.append(current_top)
                    sub_map.setdefault(current_top, [])
    except:
        pass
    top_level.sort()
    top_level.insert(0, "No Category")
    top_level.append("New Category...")
    category_menu["values"] = top_level
    if top_level:
        selected_category.set(top_level[0])
    category_menu._sub_map = sub_map
    on_category_change()

load_history()
root.update()
apply_theme(current_theme)

try:
    root.mainloop()
except:
    pass