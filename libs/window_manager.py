import customtkinter as ctk

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

# Icons
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


def make_responsive_root(root):
    root.minsize(800, 550)
    root.resizable(True, True)


def make_frame(parent, fg_color=BG, corner_radius=0):
    return ctk.CTkFrame(
        parent,
        fg_color=fg_color,
        corner_radius=corner_radius,
    )


def make_card(parent):
    return ctk.CTkFrame(
        parent,
        fg_color=SURFACE,
        border_color=BORDER,
        border_width=1,
        corner_radius=8,
    )


def make_title(parent, text, bg=BG):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=FONT_TITLE,
        text_color=GOLD,
        fg_color=bg,
    )


def make_subtitle(parent, text, bg=BG):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=FONT,
        text_color=MUTED,
        fg_color=bg,
    )


def make_section_title(parent, text, bg=SURFACE):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=FONT_LG,
        text_color=TEXT,
        fg_color=bg,
        anchor="w",
    )


def make_field_label(parent, text, bg=SURFACE):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=FONT,
        text_color=MUTED,
        fg_color=bg,
        anchor="w",
    )


def make_entry(parent, show=None):
    return ctk.CTkEntry(
        parent,
        font=FONT,
        fg_color=SURFACE2,
        text_color=TEXT,
        border_color=BORDER,
        border_width=1,
        corner_radius=6,
        show=show,
    )


def make_textbox(parent, height=100):
    return ctk.CTkTextbox(
        parent,
        height=height,
        font=FONT,
        fg_color=SURFACE2,
        text_color=TEXT,
        border_color=BORDER,
        border_width=1,
        corner_radius=6,
    )


def make_button(parent, text, command, variant="primary", font=None):
    if variant == "primary":
        fg_color = GOLD
        text_color = "#161622"
        hover_color = "#D8BA5C"
    elif variant == "danger":
        fg_color = DANGER
        text_color = "#11111B"
        hover_color = "#F07C7C"
    else:
        fg_color = SURFACE2
        text_color = TEXT
        hover_color = "#3A3A54"

    return ctk.CTkButton(
        parent,
        text=text,
        font=font or FONT,
        fg_color=fg_color,
        text_color=text_color,
        hover_color=hover_color,
        corner_radius=8,
        border_width=0,
        command=command,
    )


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


class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, parent, fg_color=BG, bg=None):
        color = fg_color if bg is None else bg

        super().__init__(
            parent,
            fg_color=color,
            corner_radius=0,
        )

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color=color,
            corner_radius=0,
            scrollbar_button_color=SURFACE2,
            scrollbar_button_hover_color="#3A3A54",
        )
        self.content.pack(fill="both", expand=True)