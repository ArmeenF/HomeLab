# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

"""
Library/Component: Known Hosts Viewer
Copyright: © 2024 ArmeenF
Description: This file contains the text vault for the Known Hosts Viewer application.
Author: ArmeenF
Documentation: For further documentation and usage examples, please refer to the README file.
"""


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
    
    
    
    
    # def create_menu(self):
    #     self.menu_bar = tk.Menu(self.root)
    #     self.root.config(menu=self.menu_bar)

    #     # File menu
    #     self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
    #     self.menu_bar.add_cascade(label="File", menu=self.file_menu)
    #     # ... your existing file menu items ...
    #     self.file_menu.add_command(
    #         label="Open", command=lambda: open_known_hosts(self.tree)
    #     )
    #     self.file_menu.add_command(label="Restart", command=lambda: restart_app(self))
    #     self.file_menu.add_separator()
    #     self.file_menu.add_command(
    #         label="About", command=lambda: about_dialog(self.root)
    #     )
    #     self.file_menu.add_command(
    #         label="Documentation", command=lambda: documentation_dialog(self.root)
    #     )
    #     self.file_menu.add_separator()
    #     self.file_menu.add_command(label="Exit", command=self.root.quit)

    #     # Add a 'Tools' or 'Actions' drop-down menu if more buttons will be added later
    #     # self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
    #     # self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
    #     # self.tools_menu.add_command(label="New Button", command=self.new_button_action)
        
        
    #     # Spacer to push the 'New Button' to the right
    #     filler = tk.Menu(self.menu_bar, tearoff=0)
    #     self.menu_bar.add_cascade(label='', menu=filler)
    #     filler.add_command(label='', state='disabled')

    #     self.menu_bar.add_command(label="New Button", command=self.new_button_action)

    # def new_button_action(self):
    #     # Placeholder for new button's functionality
    #     print("New Button Clicked!")
