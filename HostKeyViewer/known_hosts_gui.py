import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class KnownHostsViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Known Hosts Viewer")

        # Menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_known_hosts)
        self.file_menu.add_command(label="Restart", command=self.restart_app)
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

        # Style for the highlighted row
        self.tree.tag_configure("highlight", background="lawn green")

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
            initialdir="C:\\Users\\Armee\\.ssh",
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


if __name__ == "__main__":
    root = tk.Tk()
    viewer = KnownHostsViewer(root)
    root.mainloop()
