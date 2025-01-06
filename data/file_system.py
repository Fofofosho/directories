import logging
from .directory import Directory

logger = logging.getLogger("root")


class FileSystem:
    def __init__(self):
        self.root: list[Directory] = []

    def list_directories(self) -> None:
        """
        List (print) the current directories in the file system.
        """

        if not self.root:
            logger.debug("No directories in the file system")
            return

        self._traverse(self.root)

    def _traverse(self, current_location: list[Directory]) -> None:
        """
        Perform a search to find all directories and then list (print) them.
        """

        if not current_location:
            return

        # Alphabetically sort the directories before listing them
        current_location.sort(key=lambda x: x.name)

        for directory in current_location:
            whitespace = "  " * directory.depth
            logger.info(f"{whitespace}{directory.name}")
            if directory.subdirectories:
                self._traverse(directory.subdirectories)

    def add_directory_path(self, directory_path: list[str]) -> None:
        """
        Adds all of the directories to the file system from the provided path, will not create duplicates.
        """

        if not directory_path:
            raise Exception("No directory name provided")

        root_dir_name = directory_path.pop(0)
        directory = self.get_directory_from_location(root_dir_name, self.root)
        if not directory:
            parent_dir = Directory(root_dir_name, None, 0)
            self.root.append(parent_dir)
        else:
            parent_dir = directory

        for i in range(len(directory_path)):
            # i starts at 0, add 1 to the depth since we popped the root directory from the list
            depth = i + 1
            name = directory_path[i]

            sub_dir = self.get_directory_from_location(name, parent_dir.subdirectories)
            if sub_dir:
                parent_dir = sub_dir
                continue

            sub_dir = Directory(name, parent_dir, depth)

            parent_dir.add_subdirectory(sub_dir)
            parent_dir = sub_dir

    def delete_directory(self, directory_path: list[str]) -> None:
        """
        Delete a specific directory path from the file system.

        Raises an exception if directory_path is not provided.
        """

        if not directory_path:
            raise Exception("No directory path provided")

        try:
            directory = self._get_directory_by_path_or_throw(directory_path, self.root)
        except Exception as e:
            logger.warning(f"Cannot delete {'/'.join(directory_path)} - {str(e)}")
            return

        if directory:
            # Clear the subdirectories of the directory first, then delete it
            directory.clear_subdirectories()
            parent = directory.parent
            if parent:
                parent.remove_subdirectory(directory)
            else:
                # This directory doesn't have a parent because it's at the root level
                self.root.remove(directory)

    def get_directory_from_location(
        self, name: str, current_location: list[Directory]
    ) -> Directory:
        """
        Gets a directory in the current location.

        Returns None if not found.
        """

        if not current_location:
            return None

        for directory in current_location:
            if name == directory.name:
                return directory

        return None

    def move_directory(
        self, existing_path: list[str], destination_path: list[str]
    ) -> None:
        try:
            existing_directory = self._get_directory_by_path_or_throw(
                existing_path, self.root
            )
        except Exception as e:
            logger.warning(f"Cannot move {'/'.join(existing_path)} - {str(e)}")
            return

        try:
            destination_directory = self._get_directory_by_path_or_throw(
                destination_path, self.root
            )
        except Exception as e:
            logger.warning(f"Cannot move {'/'.join(destination_path)} - {str(e)}")
            return

        if existing_directory and destination_directory:
            # Check if the destination directory is a subdirectory of the existing directory
            is_subdirectory = "/".join(destination_path).startswith(
                "/".join(existing_path)
            )
            if is_subdirectory:
                logger.warning(
                    f"Cannot move {'/'.join(existing_path)} to {'/'.join(destination_path)} - destination is a subdirectory"
                )
                return

            is_root_level = existing_directory in self.root
            if is_root_level:
                # The existing directory's parent doesn't exist because it's at the root level
                self.root.remove(existing_directory)

            existing_directory.move_to(destination_directory)

    def _get_directory_by_path_or_throw(
        self, directory_path: list[str], current_location: list[Directory]
    ) -> Directory:
        """
        Recursively find the directory from the full path.

        Raises an exception if any directory in the path is not found.

        Returns the directory if found.
        """

        directory_name = directory_path[0]

        for directory in current_location:
            if directory_name == directory.name:
                if len(directory_path) == 1:
                    return directory
                else:
                    return self._get_directory_by_path_or_throw(
                        directory_path[1:], directory.subdirectories
                    )

        raise Exception(f"{directory_name} does not exist")
