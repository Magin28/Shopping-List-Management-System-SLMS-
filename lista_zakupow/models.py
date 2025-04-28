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
