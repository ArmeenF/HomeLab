"""
Library/Component: HostKeyViewer
Copyright: © 2024 ArmeenF
Description: This file contains the helper functions for the Known Hosts Viewer application.
Author: ArmeenF
Documentation: For further documentation and usage examples, please refer to the README file.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox


def restart_app(instance):
    instance.root.destroy()  # Close current window
    instance.root = tk.Tk()  # Create a new one
    instance.__init__(instance.root)  # Reinitialize the application


def open_known_hosts(tree):
    filepath = filedialog.askopenfilename(
        initialdir=os.path.expanduser("~/.ssh"),
        defaultextension=".txt",
        filetypes=[("All files", "*.*")],
    )
    if not filepath:
        return

    try:
        with open(filepath, "r") as file:
            # Clear current content
            for row in tree.get_children():
                tree.delete(row)

            for line in file:
                parts = line.strip().split(" ", 2)
                if len(parts) >= 2:
                    ip, key = parts[0], " ".join(parts[1:])
                    tree.insert("", tk.END, values=("", ip, key), tags=("unchecked",))
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file due to: {str(e)}")


def toggle_checkbox(tree, event):
    item = tree.identify_row(event.y)
    if not item:
        return

    if "unchecked" in tree.item(item, "tags"):
        tree.item(item, tags=("checked", "highlight"))
        update_visual_marker(tree, item, action="check")
    else:
        tree.item(item, tags=("unchecked",))
        update_visual_marker(tree, item, action="uncheck")


def update_visual_marker(tree, item, action="check"):
    if action == "check":
        # Update the first value in the `values` tuple with a checkmark (or any other marker).
        tree.item(item, values=("✔", *tree.item(item)["values"][1:]))
    else:
        # Remove the checkmark
        tree.item(item, values=("", *tree.item(item)["values"][1:]))


def about_dialog(parent):
    about_window = tk.Toplevel(parent)
    about_window.title("About Known Hosts Viewer")
    about_window.geometry("300x150")

    about_text = "Known Hosts Viewer\nVersion 1.0\n© 2024 ArmeenF"
    tk.Label(about_window, text=about_text, justify=tk.CENTER, padx=10, pady=10).pack()

    tk.Button(
        about_window,
        text="Close",
        command=about_window.destroy,
        background="#E1E1E1",
        relief="raised",
    ).pack(pady=10)


def documentation_dialog(parent):
    documentation_window = tk.Toplevel(parent)
    documentation_window.title("Documentation")
    documentation_window.geometry("500x400")  # Adjust size as needed

    # Create a scrollbar
    scrollbar = tk.Scrollbar(documentation_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a text widget with a scrollbar
    text_widget = tk.Text(
        documentation_window,
        wrap=tk.WORD,
        yscrollcommand=scrollbar.set,
        padx=10,
        pady=10,
    )
    text_widget.pack(expand=True, fill=tk.BOTH)

    # Configure the scrollbar
    scrollbar.config(command=text_widget.yview)

    # Documentation text content
    documentation_text = """
   Known Hosts Viewer Application Summary
    The Known Hosts Viewer is a user-friendly desktop application designed to help users manage and view their SSH known hosts file in a convenient and intuitive graphical interface. This application is built using Python's Tkinter library, ensuring cross-platform compatibility for users on different operating systems.

    Current Features
    - Open Known Hosts File: Users can easily open and view the contents of their known hosts file through a file dialog. This feature supports navigating the file system and selecting the desired file for viewing, making it easier to manage SSH connections and their corresponding keys.

    Planned Features
    - Row Selection and Deletion: A future update will allow users to select specific rows in the Treeview and delete them. This functionality will enable users to manage their known hosts file directly from the application, removing outdated or unwanted entries without manually editing the file.
    - File Updating: Following the deletion of entries, the application will automatically update the known hosts file, ensuring that changes made within the GUI are reflected in the actual file. This feature will simplify the management of SSH known hosts, making it safer and more accessible for users who may not be comfortable editing system files manually.

    Usage Scenario
    The Known Hosts Viewer is ideal for system administrators, developers, and IT professionals who frequently manage SSH connections and need a more efficient way to manage their known hosts file. By providing a graphical interface for viewing and future editing of the file, the application reduces the risk of manual errors and improves the user's workflow.

    Conclusion
    The Known Hosts Viewer combines ease of use with practical functionality for managing SSH known hosts files. Its current features provide a solid foundation for file viewing, and the planned updates will significantly enhance its capabilities for direct file management. This application is set to become an indispensable tool for anyone looking to streamline their SSH connection management process.
    """
    # Insert the documentation text into the text widget and disable editing
    text_widget.insert(tk.END, documentation_text.strip())
    text_widget.config(state=tk.DISABLED)

    # Add a button to close the dialog
    close_button = tk.Button(
        documentation_window,
        text="Close",
        command=documentation_window.destroy,
        background="#E1E1E1",
        relief="raised",
    )
    close_button.pack(pady=10)
