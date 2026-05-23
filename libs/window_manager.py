import tkinter as tk

# Core colors
BG = "#1E1E2E"
SURFACE = "#2A2A3E"
SURFACE2 = "#313148"
BORDER = "#44445A"
GOLD = "#C9A84C"
TEXT = "#E8E6F0"
MUTED = "#8A8AA8"
DANGER = "#E06B6B"
SUCCESS = "#6DB86D"

# Fonts
FONT = ("Segoe UI", 11)
FONT_SM = ("Segoe UI", 9)
FONT_LG = ("Segoe UI", 14, "bold")
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_DISPLAY = ("Segoe UI", 28, "bold")
FONT_MONO = ("Consolas", 13)

# Spacing
PAD_X = 54
PAD_Y = 42
CARD_PAD_X = 24
CARD_PAD_Y = 24
BTN_PAD_X = 24
BTN_PAD_Y = 8

# Text icons used across the app
ICON_SNAKE = "🐍"
ICON_LOCK = "🔒"
ICON_UNLOCK = "🔓"
ICON_KEY = "🔑"
ICON_REFRESH = "🔄"
ICON_WARNING = "⚠️"
ICON_FOLDER = "📁"
ICON_CLOCK = "⏱️"
ICON_COPY = "📋"
ICON_DELETE = "🗑️"
ICON_SEARCH = "⌕"
ICON_SETTINGS = "⚙️"
ICON_GENERATOR = "✦"
ICON_PLUS = "+"
ICON_BACK = "←"


def make_title(parent, text, bg=BG):
    return tk.Label(
        parent,
        text=text,
        font=FONT_TITLE,
        fg=GOLD,
        bg=bg,
    )


def make_subtitle(parent, text, bg=BG):
    return tk.Label(
        parent,
        text=text,
        font=FONT,
        fg=MUTED,
        bg=bg,
    )


def make_section_title(parent, text, bg=SURFACE):
    return tk.Label(
        parent,
        text=text,
        font=FONT_LG,
        fg=TEXT,
        bg=bg,
        anchor="w",
    )


def make_field_label(parent, text, bg=SURFACE):
    return tk.Label(
        parent,
        text=text,
        font=FONT,
        fg=MUTED,
        bg=bg,
        anchor="w",
    )


def make_card(parent):
    return tk.Frame(
        parent,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1,
    )


def make_entry(parent, show=None):
    return tk.Entry(
        parent,
        font=FONT,
        bg=SURFACE2,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        show=show,
    )


def make_button(parent, text, command, variant="primary", font=None):
    if variant == "primary":
        bg = GOLD
        fg = "#161622"
        active_bg = "#D8BA5C"
    elif variant == "danger":
        bg = DANGER
        fg = "#11111B"
        active_bg = "#F07C7C"
    else:
        bg = SURFACE2
        fg = TEXT
        active_bg = "#3A3A54"

    return tk.Button(
        parent,
        text=text,
        font=font or FONT,
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=fg,
        bd=0,
        command=command,
    )


def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()


def center_window(root, width=800, height=550):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    root.geometry(f"{width}x{height}+{x}+{y}")


def make_responsive_root(root):
    root.minsize(800, 550)
    root.resizable(True, True)