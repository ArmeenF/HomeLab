# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=unnecessary-dunder-call
# pylint: disable=broad-exception-caught


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
from text_vault import documentation_text


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
        with open(filepath, "r", encoding="utf-8") as file:
            # Clear current content
            for row in tree.get_children():
                tree.delete(row)

            for line in file:
                parts = line.strip().split(" ", 2)
                if len(parts) >= 2:
                    ip, key = parts[0], " ".join(parts[1:])
                    tree.insert("", tk.END, values=("", ip, key), tags=("unchecked",))
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"File not found: {str(e)}")
    except IOError as e:
        messagebox.showerror("Error", f"IO error occurred: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


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
    documentation_window.geometry("500x800")  # Adjust size as needed

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


def delete_selected_rows(tree):
    selected_items = tree.selection()
    selected_ips = [tree.item(item, "values")[1] for item in selected_items]

    # First, make a list of all items to delete to avoid any modification issues during iteration
    items_to_delete = list(selected_items)

    # Remove selected items from GUI
    for item in items_to_delete:
        tree.delete(item)

    # Update the known_hosts file
    known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")
    with open(known_hosts_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(known_hosts_path, "w", encoding="utf-8") as file:
        for line in lines:
            if not any(ip in line for ip in selected_ips):
                file.write(line)
