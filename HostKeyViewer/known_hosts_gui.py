# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

"""
Library/Component: HostKeyViewer
Copyright: © 2024 ArmeenF
Description: This file contains the implementation of the KnownHostsViewer class.
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
    # delete_button_action,
    delete_selected_rows,
)


class KnownHostsViewer:
    def __init__(self, root_param):
        self.root = root_param
        self.configure_root()
        self.create_menu()
        self.configure_style()
        self.setup_bottom_frame()
        self.setup_treeview()
        self.setup_scrollbar()

    def configure_root(self):
        self.root.title("Known Hosts Viewer")
        self.root.geometry("800x600")
        self.root.option_add("*Menu.font", ("JetBrains Mono", 10))

    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

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
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def configure_style(self):
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            font=("JetBrains Mono Bold", 10),
            background="#E1E1E1",
            relief="raised",
        )
        style.map(
            "Treeview",
            background=[("selected", "lightgray")],
            foreground=[("selected", "black")],
        )

    def setup_bottom_frame(self):
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        # Add and style the button
        styled_button = tk.Button(
            bottom_frame,
            text="Delete Selected",
            # command=delete_button_action,
            command=lambda: delete_selected_rows(self.tree),
            bg="red",
            highlightthickness=10,
            bd=6,
        )
        styled_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def delete_button_action(self):
        # Placeholder for your button's functionality
        print("New Bottom Button Clicked!")

    def setup_treeview(self):
        self.tree = ttk.Treeview(
            self.root,
            columns=("Select", "IP", "Key"),
            show="headings",
            selectmode="extended",
        )

        self.tree.heading("#1", text="Select", anchor=tk.W)
        self.tree.heading("IP", text="IP Address", anchor=tk.W)
        self.tree.heading("Key", text="SSH Key", anchor=tk.W)
        self.tree.column("#1", width=60, stretch=tk.NO)
        self.tree.column("IP", width=150, stretch=tk.NO)
        self.tree.column("Key", stretch=tk.YES)
        self.tree.bind("<Button-1>", lambda event: toggle_checkbox(self.tree, event))
        self.tree.pack(fill=tk.BOTH, expand=1)

    def setup_scrollbar(self):
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
    img = tk.PhotoImage(file=r"HostKeyViewer\Image\ssh.png")
    root.iconphoto(False, img)
    root.title("SSH Host Key Viewer")
    # -------------------------------------------------------- #
    viewer = KnownHostsViewer(root)
    root.mainloop()
