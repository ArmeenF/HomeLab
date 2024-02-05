import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, filedialog, messagebox


class KnownHostsViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Known Hosts Viewer")
        self.root.geometry("800x600")

        # Set the font for all Menu widgets to 'JetBrains' with a size of 10
        self.root.option_add("*Menu.font", ("JetBrains Mono", 10))

        # Menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_known_hosts)
        self.file_menu.add_command(label="Restart", command=self.restart_app)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="About", command=self.about_dialog)
        self.file_menu.add_command(
            label="Documentation", command=self.documentation_dialog
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Treeview for known_hosts
        self.tree = ttk.Treeview(
            self.root, columns=("Select", "IP", "Key"), show="headings"
        )

        # Adding the checkbox column
        self.tree.heading("#1", text="Select", anchor=tk.W)  # Align left
        self.tree.heading("IP", text="IP Address", anchor=tk.W)  # Align left
        self.tree.heading("Key", text="SSH Key", anchor=tk.W)  # Align left

        # Setting column widths and behavior
        self.tree.column("#1", width=60, stretch=tk.NO)
        self.tree.column("IP", width=150, stretch=tk.NO)
        self.tree.column("Key", stretch=tk.YES)

        # Bind checkbox event
        self.tree.tag_bind("unchecked", "<Button-1>", self.toggle_checkbox)
        self.tree.tag_bind("checked", "<Button-1>", self.toggle_checkbox)

        # Configure style for Treeview selection
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            font=("JetBrains Mono Bold", 10),
            background="#E1E1E1",
            relief="raised",
        )
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

    def toggle_checkbox(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return

        if "unchecked" in self.tree.item(item, "tags"):
            self.tree.item(item, tags=("checked", "highlight"))
            self.update_visual_marker(item, action="check")
        else:
            self.tree.item(item, tags=("unchecked",))
            self.update_visual_marker(item, action="uncheck")

    def update_visual_marker(self, item, action="check"):
        if action == "check":
            # Update the first value in the `values` tuple with a checkmark (or any other marker).
            self.tree.item(item, values=("✔", *self.tree.item(item)["values"][1:]))
        else:
            # Remove the checkmark
            self.tree.item(item, values=("", *self.tree.item(item)["values"][1:]))

    def open_known_hosts(self):
        filepath = filedialog.askopenfilename(
            # initialdir="C:\\Users\\Armee\\.ssh",
            initialdir=os.path.expanduser("~/.ssh"),
            defaultextension=".txt",
            filetypes=[("All files", "*.*")],
        )
        if not filepath:
            return

        try:
            with open(filepath, "r") as file:
                # Clear current content
                for row in self.tree.get_children():
                    self.tree.delete(row)

                for line in file:
                    parts = line.strip().split(" ", 2)
                    if len(parts) >= 2:
                        ip, key_type, key = parts[0], parts[1], " ".join(parts[1:])
                        self.tree.insert(
                            "", tk.END, values=("", ip, key), tags=("unchecked",)
                        )
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file due to: {str(e)}")

    def restart_app(self):
        self.root.destroy()  # Close current window
        self.__init__(tk.Tk())  # Create a new one

    def about_dialog(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About Known Hosts Viewer")
        about_window.geometry("300x150")

        about_text = "Known Hosts Viewer\nVersion 1.0\n© 2024 ArmeenF"
        tk.Label(
            about_window, text=about_text, justify=tk.CENTER, padx=10, pady=10
        ).pack()

        tk.Button(
            about_window,
            text="Close",
            command=about_window.destroy,
            background="#E1E1E1",
            relief="raised",
        ).pack(pady=10)

    def documentation_dialog(self):
        documentation_window = tk.Toplevel(self.root)
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
        text_widget.insert(tk.END, documentation_text)
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


if __name__ == "__main__":
    root = tk.Tk()
    # Define the default font for all widgets
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(family="JetBrains Mono Bold", size=12)
    viewer = KnownHostsViewer(root)
    root.mainloop()
