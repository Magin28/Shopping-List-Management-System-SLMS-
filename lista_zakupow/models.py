import json
import os

class Product:
    def __init__(self, name, category):
        self.name = name
        self.category = category

class ShoppingList:
    def __init__(self):
        self.lists = {}
        self.current_theme = "light"
        self.load_data()

    def add_list(self, list_name):
        if list_name not in self.lists:
            self.lists[list_name] = []
            return True
        return False

    def add_product(self, list_name, product_name, category):
        if list_name in self.lists:
            self.lists[list_name].append(Product(product_name, category))
            return True
        return False
        
    def delete_product(self, list_name, product_name, category):
    if list_name in self.lists:
        for i, p in enumerate(self.lists[list_name]):
            if p.name == product_name and p.category == category:
                del self.lists[list_name][i]
                return True
    return False


    def delete_list(self, list_name):
        if list_name in self.lists:
            del self.lists[list_name]
            return True
        return False

    def save_data(self):
        data = {
            "theme": self.current_theme,
            "lists": {name: [{"name": p.name, "category": p.category} for p in products]
                      for name, products in self.lists.items()}
        }
        with open("shopping_lists.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists("shopping_lists.json"):
            with open("shopping_lists.json", "r") as f:
                try:
                    data = json.load(f)
                    self.current_theme = data.get("theme", "light")
                    self.lists = {
                        name: [Product(p["name"], p["category"]) for p in products]
                        for name, products in data.get("lists", {}).items()
                    }
                except Exception as e:
                    print(f"Błąd ładowania danych: {str(e)}")
                    self.lists = {}
        else:
            self.lists = {}
