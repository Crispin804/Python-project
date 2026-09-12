Here is the updated README.md file, stripped of embedded Python code and restructured to reference shop_app.py directly.

Shop Inventory Management System
A Python-based desktop application designed for shopkeepers to manage inventory. Features full CRUD (Create, Read, Update, Delete) capabilities, table visual views, and database persistence using Python, Tkinter, and SQLite.

Prerequisites & Installation
Follow these steps to set up your environment before running the project.

Step 1: Install Python
Python 3 includes both Tkinter (the GUI library) and SQLite3 (the database driver) in its standard library.

Windows
Download the latest Python installer from python.org.

Run the installer and ensure "Add Python to PATH" is checked before clicking Install.

Verify installation in Command Prompt:

DOS
python --version
macOS
Install Python using Homebrew:

Bash
brew install python
Verify installation in Terminal:

Bash
python3 --version
Linux (Ubuntu/Debian)
Update system packages and install Python along with Tkinter support:

Bash
sudo apt update
sudo apt install python3 python3-tk -y
Verify installation in Terminal:

Bash
python3 --version
Step 2: Install SQLite Database Engine (Optional CLI Tool)
Python manages SQLite database files directly through code without requiring external server installations. However, if you want an external tool to manually inspect or view the .db file:

SQLite CLI / DB Browser: Download DB Browser for SQLite (GUI) or install via terminal:

Ubuntu/Debian: sudo apt install sqlite3

macOS: brew install sqlite

File Creation & Project Setup
Follow these steps to create and structure your project files.

1. Create the Project Directory
Open your command line or terminal and run:

Bash
mkdir shop_inventory_system
cd shop_inventory_system
2. Create the Project Files
Create the core files in your project directory:

shop_app.py — Holds the main Python application code containing the Database and ShopApp classes.

README.md — Project documentation.

Folder Structure
Once created, your project directory should look like this:

Plaintext
shop_inventory_system/
│
├── shop_app.py           # Main application source code
├── README.md             # Documentation file
└── shop_inventory.db     # Auto-generated SQLite file (created on first run)
Running the Application
Execute the script from your terminal:

Windows:

DOS
python shop_app.py
macOS / Linux:

Bash
python3 shop_app.py
Upon initial run, the application creates shop_inventory.db in the working directory automatically.

Operating Instructions
Add Item: Enter Name, Quantity, and Price, then click Add Item.

Read / View Table: All items appear automatically in the table view below the form.

Update Item: Click a row in the table to load its data into the input form. Make modifications and click Update Selected.

Delete Item: Click a row in the table, click Delete Selected, and confirm the prompt.

Fetch Names: Click Show Item Names to pop up a dialog displaying only item names from the database.
