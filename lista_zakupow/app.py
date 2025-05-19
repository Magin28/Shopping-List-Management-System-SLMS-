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
    def add_list(self):
        list_name = self.list_entry.get()
        if list_name and self.shopping_list.add_list(list_name):
            self.update_combobox()
            self.list_entry.delete(0, tk.END)
            messagebox.showinfo("Sukces", f"Lista '{list_name}' dodana!")
        else:
            messagebox.showwarning("Uwaga", "Lista już istnieje!")

    def add_product(self):
        list_name = self.current_list.get()
        product = self.product_entry.get()
        category = self.category_combobox.get()
        if list_name and product and category:
            if self.shopping_list.add_product(list_name, product, category):
                self.update_display()
                self.product_entry.delete(0, tk.END)
                self.category_combobox.set('')

    def update_display(self):
        self.tree.delete(*self.tree.get_children())
        if list_name := self.current_list.get():
            for idx, product in enumerate(self.shopping_list.lists.get(list_name, [])):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=(product.name, product.category), tags=(tag,))

    def update_combobox(self):
        lists = list(self.shopping_list.lists.keys())
        self.list_combobox["values"] = lists
        if lists:
            self.current_list.set(lists[0])

    def delete_list(self):
        if (list_name := self.current_list.get()) and messagebox.askyesno("Potwierdź", f"Usunąć listę '{list_name}'?"):
            self.shopping_list.delete_list(list_name)
            self.update_combobox()
            self.update_display()
    def save_list(self):
        self.shopping_list.save_data()
        messagebox.showinfo("Sukces", "Dane zapisane!")

    def load_data(self):
        self.shopping_list.load_data()
        self.update_combobox()
        self.update_display()

    def save_to_txt(self):
        if not (list_name := self.current_list.get()):
            messagebox.showerror("Błąd", "Wybierz listę do eksportu!")
            return
        if file_path := filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")], initialfile=f"{list_name}.txt"):
            exporter.export_to_txt(list_name, self.shopping_list.lists[list_name], file_path)
            messagebox.showinfo("Sukces", "Lista zapisana do TXT!")

    def save_to_pdf(self):
        if not (list_name := self.current_list.get()):
            messagebox.showerror("Błąd", "Wybierz listę do eksportu!")
            return
        if file_path := filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Pliki PDF", "*.pdf")], initialfile=f"{list_name}.pdf"):
            exporter.export_to_pdf(list_name, self.shopping_list.lists[list_name], file_path)
            messagebox.showinfo("Sukces", "Lista zapisana do PDF!")

    def on_close(self):
        self.shopping_list.save_data()
        self.destroy()
