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
