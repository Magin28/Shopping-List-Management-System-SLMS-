import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from theme_manager import ThemeManager
from models import ShoppingList
import exporter

class ModernShoppingListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Shopping List")
        self.geometry("1280x800")
        self.shopping_list = ShoppingList()
        self.current_list = tk.StringVar()
        self.theme = ThemeManager.get_themes()[self.shopping_list.current_theme]

        self._create_widgets()
        self._configure_styles()
        self.load_data()
        self.update_theme()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        theme = self.theme
        self.style.configure("TFrame", background=theme["bg"])
        self.style.configure("TLabel", background=theme["bg"], foreground=theme["fg"], font=("Segoe UI", 10))
        self.style.configure("TButton", background=theme["accent"], foreground=theme["fg"], borderwidth=0, font=("Segoe UI", 10), padding=8)
        self.style.map("TButton", background=[("active", theme["hover"])])
        self.style.configure("Treeview.Heading", background=theme["header_bg"], foreground=theme["header_fg"], font=("Segoe UI", 11, "bold"), padding=6)
        self.style.configure("Treeview", background=theme["tree_bg"], foreground=theme["tree_fg"], fieldbackground=theme["tree_bg"], font=("Segoe UI", 11), rowheight=30)
        self.style.configure("TCombobox", fieldbackground=theme["widget_bg"], background=theme["widget_bg"], foreground=theme["text"])
        self.style.configure("TEntry", fieldbackground=theme["widget_bg"], foreground=theme["text"])

    def update_theme(self):
        self.theme = ThemeManager.get_themes()[self.shopping_list.current_theme]
        self.configure(background=self.theme["bg"])
        self._configure_styles()
        self._update_widget_colors()

    def _update_widget_colors(self):
        for widget in [self.main_frame, self.header_frame, self.content_frame, self.left_panel, self.right_panel, self.form_frame, self.footer_frame]:
            widget.configure(style="TFrame")
        self.tree.tag_configure("oddrow", background=self.theme["secondary_bg"])
        self.tree.tag_configure("evenrow", background=self.theme["bg"])
        self.title_label.configure(foreground=self.theme["fg"])
        self.theme_button.configure(text="🌙" if self.shopping_list.current_theme == "light" else "☀️")

    def toggle_theme(self):
        self.shopping_list.current_theme = "dark" if self.shopping_list.current_theme == "light" else "light"
        self.update_theme()
        self.shopping_list.save_data()