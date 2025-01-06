import logging

logger = logging.getLogger("root")


class Directory:
    def __init__(self, name: str, parent: "Directory" = None, depth: int = 0):
        self.name = name
        self.parent = parent
        self.subdirectories: list[Directory] = []
        self.depth = depth

    def add_subdirectory(self, subdirectory: "Directory") -> None:
        """
        Add a provided subdirectory to the current directory.

        Raises an exception if the subdirectory already exists.
        """

        for child in self.subdirectories:
            if child.name == subdirectory.name:
                raise Exception(f"Directory {subdirectory.name} already exists")

        self.subdirectories.append(subdirectory)

    def move_to(self, parent: "Directory") -> None:
        """
        Update the parent directory of the current directory, also update the depth of all subdirectories.
        """

        # Add the current directory to the new parent first to avoid duplicate directory exceptions
        parent.add_subdirectory(self)
        if self.parent:
            self.parent.remove_subdirectory(self)

        self.parent = parent
        self.update_depth(parent.depth + 1)

    def update_depth(self, depth: int) -> None:
        """
        Update the depth of the current directory and all subdirectories.
        """

        self.depth = depth

        for child in self.subdirectories:
            child.update_depth(depth + 1)

    def remove_subdirectory(self, subdirectory: "Directory") -> None:
        """
        Remove a specific subdirectory from the current directory.

        Does nothing if the subdirectory does not exist.
        """

        for child in self.subdirectories:
            if child.name == subdirectory.name:
                self.subdirectories.remove(child)

    def clear_subdirectories(self) -> None:
        """
        Recursively remove all subdirectories from the current directory.
        """

        if not self.subdirectories:
            return

        for child in self.subdirectories:
            child.clear_subdirectories()

        self.subdirectories.clear()
