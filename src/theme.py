from tkinter import ttk

class Theme:
    """Minimalist pastel theme"""
    COLORS = {
        'bg_primary': '#F5F5F0', 'bg_secondary': '#E8E4E0',
        'bg_panel': '#FAF8F5', 'bg_input': '#FEFEFE',
        'accent_primary': '#9BB5B0', 'accent_secondary': '#D4A5A5',
        'accent_tertiary': '#B5B0C9', 'success': '#A8C5A6',
        'text_primary': '#3A3A38', 'text_secondary': '#6B6B68',
        'text_accent': '#7A8B88', 'warning': '#D9A89F',
        'border': '#D5D0C8', 'hover': '#C8C3BB'
    }

    @staticmethod
    def configure_style():
        style = ttk.Style()
        c = Theme.COLORS

        style.configure('Pastel.TFrame', background=c['bg_primary'], relief='flat')
        style.configure('Panel.TFrame', background=c['bg_panel'], relief='flat')
        style.configure('Pastel.TLabel', background=c['bg_primary'],
                        foreground=c['text_primary'], font=('Helvetica Neue', 10))
        style.configure('Title.TLabel', background=c['bg_primary'],
                        foreground=c['text_primary'], font=('Helvetica Neue', 16))
        style.configure('Header.TLabel', background=c['bg_primary'],
                        foreground=c['text_accent'], font=('Helvetica Neue', 11))
        style.configure('Pastel.TButton', background=c['accent_primary'],
                        foreground=c['text_primary'], font=('Helvetica Neue', 9),
                        borderwidth=1, relief='flat', padding=(10, 5))
        style.map('Pastel.TButton', background=[('active', c['hover']), ('pressed', c['accent_secondary'])])
        style.configure('Pastel.TNotebook', background=c['bg_primary'], borderwidth=0)
        style.configure('Pastel.TNotebook.Tab', background=c['bg_secondary'],
                        foreground=c['text_secondary'], padding=[14, 6],
                        font=('Helvetica Neue', 9), borderwidth=0)
        style.map('Pastel.TNotebook.Tab',
                  background=[('selected', c['bg_primary']), ('active', c['hover'])],
                  foreground=[('selected', c['text_primary'])])
        return style
