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
        
    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", padx=20, pady=10)

        self.title_label = ttk.Label(self.header_frame, text="🛒 Smart Shopping List", font=("Segoe UI", 18, "bold"))
        self.title_label.pack(side="left")

        self.theme_button = ttk.Button(self.header_frame, text="🌙", command=self.toggle_theme, width=3)
        self.theme_button.pack(side="right", padx=5)

        # Main content
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel
        self.left_panel = ttk.Frame(self.content_frame, width=280)
        self.left_panel.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(self.left_panel, text="Nowa lista:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.list_entry = ttk.Entry(self.left_panel, width=25, font=("Segoe UI", 10))
        self.list_entry.pack(pady=5, fill="x")
        ttk.Button(self.left_panel, text="➕ Dodaj listę", command=self.add_list).pack(pady=5, fill="x")

        ttk.Separator(self.left_panel, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(self.left_panel, text="Aktywne listy:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.list_combobox = ttk.Combobox(self.left_panel, textvariable=self.current_list, state="readonly", width=23, font=("Segoe UI", 10))
        self.list_combobox.pack(pady=5, fill="x")
        ttk.Button(self.left_panel, text="🗑️ Usuń listę", command=self.delete_list).pack(pady=5, fill="x")

        # Right panel
        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Product form
        self.form_frame = ttk.Frame(self.right_panel)
        self.form_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(self.form_frame, text="Produkt:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
        self.product_entry = ttk.Entry(self.form_frame, width=25, font=("Segoe UI", 10))
        self.product_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.form_frame, text="Kategoria:", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5)
        self.category_combobox = ttk.Combobox(self.form_frame, values=["Nabiał", "Pieczywo", "Warzywa", "Mięso", "Inne"], width=18, font=("Segoe UI", 10))
        self.category_combobox.grid(row=0, column=3, padx=5)

        ttk.Button(self.form_frame, text="➕ Dodaj produkt", command=self.add_product).grid(row=0, column=4, padx=10)

        # Products table
        self.tree = ttk.Treeview(self.right_panel, columns=("product", "category"), show="headings")
        self.tree.heading("product", text="Produkt")
        self.tree.heading("category", text="Kategoria")
        self.tree.column("product", width=300, anchor="w")
        self.tree.column("category", width=200, anchor="w")
        self.tree.pack(fill="both", expand=True)

        # Footer
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 10))
        ttk.Button(self.footer_frame, text="💾 Zapisz wszystko", command=self.save_list).pack(side="left", padx=5)
        ttk.Button(self.footer_frame, text="📄 Eksportuj do TXT", command=self.save_to_txt).pack(side="left", padx=5)
        ttk.Button(self.footer_frame, text="📊 Eksportuj do PDF", command=self.save_to_pdf).pack(side="left", padx=5)
        ttk.Button(self.footer_frame, text="⟳ Odśwież", command=self.update_display).pack(side="right", padx=5)
