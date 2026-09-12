import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class Database:

    """Handles all database connections and SQL operations."""

    def __init__(self, db_name="shop_inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_item(self, name, quantity, price):
        query = "INSERT INTO items (item_name, quantity, price) VALUES (?, ?, ?)"
        self.cursor.execute(query, (name, quantity, price))
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM items")
        return self.cursor.fetchall()

    def fetch_names_only(self):
        self.cursor.execute("SELECT item_name FROM items")
        return [row[0] for row in self.cursor.fetchall()]

    def update_item(self, item_id, name, quantity, price):
        query = "UPDATE items SET item_name=?, quantity=?, price=? WHERE id=?"
        self.cursor.execute(query, (name, quantity, price, item_id))
        self.conn.commit()

    def delete_item(self, item_id):
        query = "DELETE FROM items WHERE id=?"
        self.cursor.execute(query, (item_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


class ShopApp:

    """Handles the Tkinter GUI layout, event handling, and form operations."""

    def __init__(self, root):
        self.root = root
        self.root.title("Shop Inventory Management")
        self.root.geometry("750x500")

        # Database Manager Instance
        self.db = Database()

        # Track selected item ID
        self.selected_item_id = None

        # Build Interface
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # --- Form Frame (Top) ---
        form_frame = tk.LabelFrame(
            self.root, text="Item Entry Form", font=("Arial", 11, "bold")
        )
        form_frame.pack(fill="x", padx=15, pady=10)

        # Form Inputs
        tk.Label(form_frame, text="Item Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.entry_name = tk.Entry(form_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Quantity:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )
        self.entry_quantity = tk.Entry(form_frame)
        self.entry_quantity.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Price ($):").grid(
            row=0, column=4, padx=5, pady=5, sticky="e"
        )
        self.entry_price = tk.Entry(form_frame)
        self.entry_price.grid(row=0, column=5, padx=5, pady=5)

        # --- Button Frame ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=15, pady=5)

        tk.Button(
            btn_frame,
            text="Add Item",
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self.add_item,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="Update Selected",
            bg="#2196F3",
            fg="white",
            width=12,
            command=self.update_item,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="Delete Selected",
            bg="#f44336",
            fg="white",
            width=12,
            command=self.delete_item,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="Clear Form",
            bg="#757575",
            fg="white",
            width=12,
            command=self.clear_form,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="Show Item Names",
            bg="#FF9800",
            fg="white",
            width=15,
            command=self.show_names,
        ).pack(side="right", padx=5)

        # --- Data Table (Bottom) ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("id", "name", "quantity", "price")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Item Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price ($)")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=250)
        self.tree.column("quantity", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="center")

        # Scrollbar for table
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind row selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # --- Controller Methods ---

    def load_data(self):
        """Fetch all records from SQLite and populate the treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        records = self.db.fetch_all()
        for record in records:
            self.tree.insert("", "end", values=record)

    def add_item(self):
        name = self.entry_name.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()

        if not name or not quantity or not price:
            messagebox.showwarning(
                "Input Error", "Please fill in all fields."
            )
            return

        try:
            self.db.add_item(name, int(quantity), float(price))
            messagebox.showinfo("Success", "Item added successfully!")
            self.clear_form()
            self.load_data()
        except ValueError:
            messagebox.showerror(
                "Value Error", "Quantity must be an integer and Price a number."
            )

    def on_row_select(self, event):
        """Fills the form entries when a user selects a table row."""
        selected_row = self.tree.focus()
        if not selected_row:
            return

        values = self.tree.item(selected_row, "values")
        self.selected_item_id = values[0]

        self.clear_form()
        self.entry_name.insert(0, values[1])
        self.entry_quantity.insert(0, values[2])
        self.entry_price.insert(0, values[3])

    def update_item(self):
        if not self.selected_item_id:
            messagebox.showwarning(
                "Selection Error", "Please select an item from the table first."
            )
            return

        name = self.entry_name.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()

        if not name or not quantity or not price:
            messagebox.showwarning("Input Error", "Fields cannot be empty.")
            return

        try:
            self.db.update_item(
                self.selected_item_id, name, int(quantity), float(price)
            )
            messagebox.showinfo("Success", "Item updated successfully!")
            self.clear_form()
            self.load_data()
        except ValueError:
            messagebox.showerror(
                "Value Error", "Quantity must be an integer and Price a number."
            )

    def delete_item(self):
        if not self.selected_item_id:
            messagebox.showwarning(
                "Selection Error",
                "Please select an item from the table to delete.",
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this item?"
        )
        if confirm:
            self.db.delete_item(self.selected_item_id)
            messagebox.showinfo("Success", "Item deleted.")
            self.clear_form()
            self.load_data()

    def show_names(self):
        """Fetches and displays only item names in a popup dialog."""
        names = self.db.fetch_names_only()
        if not names:
            messagebox.showinfo("Item Names", "No items currently in inventory.")
            return

        formatted_names = "\n".join([f"• {name}" for name in names])
        messagebox.showinfo("Registered Item Names", formatted_names)

    def clear_form(self):
        self.selected_item_id = None
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ShopApp(root)
    root.mainloop()