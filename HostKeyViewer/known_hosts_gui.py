"""
Library/Component: HostKeyViewer
Copyright: © 2024 ArmeenF
Description: This file contains the implementation of the KnownHostsViewer class, which is a graphical user interface for viewing and managing SSH known hosts.
Original Author: ArmeenF
Documentation: For further documentation and usage examples, please refer to the README file.
Usage Examples: [Provide usage examples if applicable]
"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from helper import (
    restart_app,
    open_known_hosts,
    about_dialog,
    documentation_dialog,
    toggle_checkbox,
)


class KnownHostsViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Known Hosts Viewer")
        self.root.geometry("800x600")

        # Set the font for all Menu widgets to 'JetBrains' with a size of 10
        self.root.option_add("*Menu.font", ("JetBrains Mono", 10))

        # Configure style for Treeview selection
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            font=("JetBrains Mono Bold", 10),
            background="#E1E1E1",
            relief="raised",
        )

        # Menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="Open", command=lambda: open_known_hosts(self.tree)
        )
        self.file_menu.add_command(label="Restart", command=lambda: restart_app(self))
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="About", command=lambda: about_dialog(self.root)
        )
        self.file_menu.add_command(
            label="Documentation", command=lambda: documentation_dialog(self.root)
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Treeview for known_hosts
        self.tree = ttk.Treeview(root, columns=("Select", "IP", "Key"), show="headings")

        # Adding the checkbox column
        self.tree.heading("#1", text="Select", anchor=tk.W)  # Align left
        self.tree.heading("IP", text="IP Address", anchor=tk.W)  # Align left
        self.tree.heading("Key", text="SSH Key", anchor=tk.W)  # Align left

        # Setting column widths and behavior
        self.tree.column("#1", width=60, stretch=tk.NO)
        self.tree.column("IP", width=150, stretch=tk.NO)
        self.tree.column("Key", stretch=tk.YES)

        # Bind checkbox event
        self.tree.bind("<Button-1>", lambda event: toggle_checkbox(self.tree, event))

        # Change the selection background to a lighter color but still visible
        # And optionally, change the selection foreground (text color) if needed
        style.map(
            "Treeview",
            background=[
                ("selected", "lightgray")
            ],  # Change "lightgray" to any color you prefer
            foreground=[("selected", "black")],
        )  # Change "black" to suit your preference

        self.tree.pack(fill=tk.BOTH, expand=1)

        # Scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(
            self.root, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


if __name__ == "__main__":
    root = tk.Tk()
    # -------------------------------------------------------- #
    # Define the default font for all widgets
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(family="JetBrains Mono Bold", size=12)
    # -------------------------------------------------------- #
    # Define the default icon and title for the application
    img = tk.PhotoImage(file='HostKeyViewer\Image\ssh.png')
    root.iconphoto(False, img)
    root.title("SSH Host Key Viewer")
    # -------------------------------------------------------- #
    viewer = KnownHostsViewer(root)
    root.mainloop()
