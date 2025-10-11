import tkinter as tk
from src.theme import Theme

class PrologTemplateButton(tk.Button):
    """A button that inserts Prolog template code into the editor"""

    def __init__(self, parent, template_text, label, code_widget, **kwargs):
        self.template_text = template_text
        self.code_widget = code_widget

        super().__init__(parent, text=label, command=self.insert_template,
                         bg=Theme.COLORS['bg_secondary'], fg=Theme.COLORS['text_primary'],
                         font=('Helvetica Neue', 8), relief=tk.FLAT, bd=1,
                         padx=5, pady=4, wraplength=70, justify=tk.CENTER, **kwargs)

    def insert_template(self):
        cursor_pos = self.code_widget.index(tk.INSERT)
        self.code_widget.insert(cursor_pos, self.template_text + '\n')
        new_pos = self.code_widget.index(f"{cursor_pos}+{len(self.template_text)} chars")
        self.code_widget.mark_set(tk.INSERT, new_pos)
        self.code_widget.see(tk.INSERT)
        self.code_widget.focus()
