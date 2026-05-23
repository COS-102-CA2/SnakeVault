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

# Text icons
ICON_SNAKE = "🐍"
ICON_LOCK = "🔒"
ICON_UNLOCK = "🔓"
ICON_KEY = "🔑"
ICON_REFRESH = "🔄"
ICON_WARNING = "⚠"
ICON_FOLDER = "📁"
ICON_CLOCK = "⏱"
ICON_COPY = "📋"
ICON_DELETE = "🗑"
ICON_SEARCH = "⌕"
ICON_SETTINGS = "⚙"
ICON_GENERATOR = "✦"
ICON_PLUS = "+"
ICON_BACK = "←"
ICON_EYE = "👁"
ICON_EYE_OFF = "🙈"


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
        hover_bg = "#D8BA5C"
    elif variant == "danger":
        bg = DANGER
        fg = "#11111B"
        active_bg = "#F07C7C"
        hover_bg = "#F07C7C"
    else:
        bg = SURFACE2
        fg = TEXT
        active_bg = "#3A3A54"
        hover_bg = "#3A3A54"

    button = tk.Button(
        parent,
        text=text,
        font=font or FONT,
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=fg,
        bd=0,
        relief="flat",
        cursor="hand2",
        command=command,
    )

    button.default_bg = bg
    button.hover_bg = hover_bg

    button.bind("<Enter>", lambda _event: button.configure(bg=button.hover_bg))
    button.bind("<Leave>", lambda _event: button.configure(bg=button.default_bg))

    return button


def make_icon_button(parent, text, command, variant="secondary"):
    return make_button(
        parent,
        text,
        command,
        variant=variant,
        font=FONT,
    )


def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()


def make_responsive_root(root):
    root.minsize(800, 550)
    root.resizable(True, True)


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg=BG):
        super().__init__(parent, bg=bg)

        self.canvas = tk.Canvas(
            self,
            bg=bg,
            highlightthickness=0,
            bd=0,
        )
        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.content = tk.Frame(self.canvas, bg=bg)

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw",
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.content.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.resize_content)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_content(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")