import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QPushButton, QFileDialog, QProgressBar, QMenu, QAction, QHBoxLayout, QLabel, QLineEdit, QComboBox
)
from PyQt5.QtCore import QSettings, Qt, QTimer
from PyQt5.QtGui import QFont
from androguard import util
from androguard.core.apk import get_apkid
import os




util.set_log("CRITICAL")


settings = QSettings("APKPackageViewer", "APKPackageViewer")

def get_list_of_package_names(folder):
    package_dict = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.apk'):
                file_path = os.path.abspath(os.path.join(root, file))
                try:
                    package_name = get_apkid(file_path)[0]
                except:
                    package_name = "Unknown"  # Set to "Unknown" in case of exception
                package_dict[file_path] = package_name
    return package_dict


def open_folder(item):
    if item:
        filepath = item.text(2)  # Index 2 corresponds to the "File Path" column
        folder_path = os.path.dirname(filepath)
        os.system(f'explorer /select,{filepath}')

def load_files_progress(folder_path, progress_bar):
    package_dict = get_list_of_package_names(folder_path)

    total_files = len(package_dict)
    progress_bar.setMaximum(total_files)
    progress_bar.setValue(0)

    count_label.setText(f"APK's Found: 0")  # Reset count label

    item = tree.invisibleRootItem()
    for index, (filepath, packagename) in enumerate(package_dict.items(), 1):
        filename = os.path.basename(filepath)
        child_item = QTreeWidgetItem([filename, packagename, filepath])
        item.addChild(child_item)

        progress_bar.setValue(index)
        count_label.setText(f"APK's Found: {index}")  # Update count label
        QApplication.processEvents()

    progress_bar.setValue(total_files)

def load_files():
    # Retrieve the last opened folder from settings
    last_folder = settings.value("last_folder", "")
    folder_path = QFileDialog.getExistingDirectory(None, "Select Folder", last_folder)

    if folder_path:
        tree.clear()

        # Reset the progress bar
        progress_bar.setValue(0)

        # Load files with progress
        load_files_progress(folder_path, progress_bar)

        # Save the parent folder as the last opened folder in settings
        parent_folder = os.path.dirname(folder_path)
        settings.setValue("last_folder", parent_folder)

def on_item_double_click(item, column):
    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
    open_folder(item)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("APK Package Viewer")

# Set the initial size of the main window
window.setGeometry(100, 100, 1080, 880)  # Adjust the size as needed

central_widget = QWidget()
window.setCentralWidget(central_widget)
layout = QVBoxLayout(central_widget)

tree = QTreeWidget()
tree.setHeaderLabels(["File Name", "Package Name", "File Path"])  # Adjusted header labels
tree.header().setSectionResizeMode(QHeaderView.Interactive)  # Allow manual resizing
layout.addWidget(tree)
# Set the initial section size to one-third of the available space
initial_section_size = window.width() // 3
tree.header().resizeSection(0, initial_section_size)
tree.header().resizeSection(1, initial_section_size)
tree.header().resizeSection(2, initial_section_size)

# Set the context menu policy to custom
tree.setContextMenuPolicy(Qt.CustomContextMenu)


# Modify the show_context_menu function to include Windows Explorer context menu items
# Modify the show_context_menu function to include "Copy as path" and "Rename" context menu items
def show_context_menu(position):
    context_menu = QMenu(tree)
    
    open_file_action = QAction("Open", tree)
    open_file_action.triggered.connect(lambda: open_file(tree.currentItem()))
    context_menu.addAction(open_file_action)
    
    # Add actions for opening the folder and loading files
    open_action = QAction("Open in Folder", tree)
    open_action.triggered.connect(lambda: open_folder(tree.currentItem()))
    context_menu.addAction(open_action)

    copy_path_action = QAction("Copy as path", tree)
    copy_path_action.triggered.connect(lambda: copy_file_path(tree.currentItem()))
    context_menu.addAction(copy_path_action)
    
    # Add "Rename" action
    rename_action = QAction("Rename", tree)
    rename_action.triggered.connect(lambda: rename_file(tree.currentItem()))
    context_menu.addAction(rename_action)


    # Add a separator between custom actions and Explorer context menu items
    # context_menu.addSeparator()

    # Show the context menu at the specified position
    context_menu.exec_(tree.viewport().mapToGlobal(position))


# Copy the file path to the clipboard
# Copy the file path to the clipboard with double quotes
def copy_file_path(item):
    if item:
        filepath = item.text(2)  # Index 2 corresponds to the "File Path" column
        if ' ' in filepath:
            filepath = f'"{filepath}"'  # Add double quotes around the file path
        clipboard = QApplication.clipboard()
        clipboard.setText(filepath)


def rename_file(item):
    if item:
        # Enable editing of the first column (File Name)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        tree.editItem(item, 0)
        
def on_item_changed(item, column):
    if column == 0:  # Check if the edited column is the "File Name" column
        new_file_name = item.text(column)
        file_path = item.text(2)  # Index 2 corresponds to the "File Path" column
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        # Rename the file on the filesystem
        try:
            os.rename(file_path, new_file_path)
        except OSError as e:
            print(f"Error renaming file: {e}")
            # You may want to handle the error in an appropriate way

        # Update the file path in the tree view
        item.setText(2, new_file_path)

# Connect the itemChanged signal to the on_item_changed function
tree.itemChanged.connect(on_item_changed)



            
def open_file(item):
    if item:
        filepath = item.text(2)  # Index 2 corresponds to the "File Path" column
        os.system(f'start {filepath}')



# Connect the custom context menu function to the customContextMenu signal
tree.customContextMenuRequested.connect(show_context_menu)



search_layout = QHBoxLayout()
search_label = QLabel("Search:")
search_layout.addWidget(search_label)

search_input = QLineEdit()
search_layout.addWidget(search_input)

field_label = QLabel("Search Field:")
search_layout.addWidget(field_label)

field_dropdown = QComboBox()
field_dropdown.addItems(["All Fields", "File Name", "Package Name", "File Path"])
search_layout.addWidget(field_dropdown)

layout.addLayout(search_layout)

# Function to handle the search
def search_files():
    search_text = search_input.text().lower()
    selected_field = field_dropdown.currentText()

    root_item = tree.invisibleRootItem()

    for i in range(root_item.childCount()):
        item = root_item.child(i)
        file_name = item.text(0).lower()
        package_name = item.text(1).lower()
        file_path = item.text(2).lower()

        if (
                (selected_field == "All Fields" and (
                search_text in file_name or
                search_text in package_name or
                search_text in file_path
            ))
            or (selected_field == "File Name" and search_text in file_name)
            or (selected_field == "Package Name" and search_text in package_name)
            or (selected_field == "File Path" and search_text in file_path)
        ):

            item.setHidden(False)
        else:
            item.setHidden(True)

# Connect the search button to the search_files function
search_button = QPushButton("Search")
search_button.clicked.connect(search_files)
# search_layout.addWidget(search_button) # no need for search button since it happens as user types

# Connect the returnPressed signal of the search_input to the search_files function
search_input.returnPressed.connect(search_files)

search_input.textChanged.connect(search_files)





load_button = QPushButton("Select Folder")
load_button.clicked.connect(load_files)
layout.addWidget(load_button)
# Create the progress bar initially
progress_bar = QProgressBar()
progress_bar.setAlignment(Qt.AlignCenter)
layout.addWidget(progress_bar)
window.show()

count_label = QLabel("APK's Found: 0")
font = QFont()
font.setBold(True)
layout.addWidget(count_label)

tree.itemDoubleClicked.connect(on_item_double_click)

sys.exit(app.exec_())
