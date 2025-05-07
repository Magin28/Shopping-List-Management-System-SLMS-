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

    def delete_list(self, list_name):
        if list_name in self.lists:
            del self.lists[list_name]
            return True
        return False