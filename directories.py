import sys

from utils.log import setup_logger
from data.file_system import FileSystem

COMMANDS = ["CREATE", "LIST", "MOVE", "DELETE"]

file_system = FileSystem()


def parse_and_validate_input(input: str) -> list[str]:
    """
    Parse and validate the input string. The input string should be in the format of [COMMAND] [ARGS]...
    """

    return_list = []

    for value in input.split(" "):
        return_list.append(value)

    validate_or_throw(return_list)

    return return_list


def validate_or_throw(args: list[str]) -> None:
    """
    Validate the input arguments against supported commands. The first argument should be a valid command.

    Raises an exception if the command and/or options provided are invalid
    """

    if len(args) == 0:
        logger.error("No arguments provided")
        raise Exception("No arguments provided")

    command = args[0].upper()
    match command:
        case "MOVE":
            if len(args) != 3:
                raise Exception(
                    "Invalid MOVE arguments. MOVE command requires current path and the destination path."
                )
        case "CREATE":
            if len(args) != 2:
                raise Exception(
                    "Invalid CREATE arguments. CREATE command requires a directory name."
                )
        case "DELETE":
            if len(args) != 2:
                raise Exception(
                    "Invalid DELETE arguments. DELETE command requires a directory name."
                )
        case "LIST":
            if len(args) != 1:
                raise Exception(
                    "Invalid LIST arguments. LIST command does not require any arguments."
                )
        case _:
            raise Exception(f"Invalid command, must be [COMMAND] [ARGS]. Input: {args}")


def handle_create(directory_name: str) -> None:
    """
    Handle the CREATE command. Split the directory name by '/' and will create directories as necessary along that path.

    Raises an exception if no directory name is provided.
    """

    if not directory_name:
        raise Exception("No directory name provided")

    names = directory_name.split("/")

    file_system.add_directory_path(names)


def handle_move(existing_path: str, destination_path: str) -> None:
    """
    Handle the MOVE command. Will move the directory at the existing path to the destination path.

    Raises an exception if the existing path or destination path is not provided.
    """

    if not existing_path or not destination_path:
        raise Exception("Missing required arguments for MOVE command")

    existing_full_path = existing_path.split("/")
    destination_full_path = destination_path.split("/")

    file_system.move_directory(existing_full_path, destination_full_path)


def handle_list() -> None:
    """
    Handle the LIST command. List all directories in the file system with proper indentation.
    """

    file_system.list_directories()


def handle_delete(directory_name: str) -> None:
    """
    Handle the DELETE command. Deletes the directory listed at the end of the path.
    """

    if not directory_name:
        raise Exception("No directory name provided")

    # Split the directory name by '/'
    full_path = directory_name.split("/")

    file_system.delete_directory(full_path)


def process_input(input: str) -> None:
    logger.info(input)

    try:
        args = parse_and_validate_input(input)
        command = args[0].upper()
        match command:
            case "CREATE":
                logger.debug("Creating directory")
                path = args[1]
                handle_create(path)

            case "LIST":
                logger.debug("Listing directories")
                handle_list()

            case "MOVE":
                logger.debug("Moving directory")
                existing_path = args[1]
                destination_path = args[2]
                handle_move(existing_path, destination_path)

            case "DELETE":
                logger.debug("Deleting directory")
                existing_path = args[1]
                handle_delete(existing_path)

            case _:
                raise Exception(
                    f"Invalid command, please use one of these commands: {COMMANDS}"
                )
    except Exception as e:
        logger.error(f"Error: {e}")


def main() -> None:
    input_args = sys.argv[1:]

    if input_args and len(input_args) == 2 and input_args[0] == "-f":
        file_name = input_args[1]
        if not file_name:
            raise Exception("File name not provided")

        with open(file_name, "r") as input_file:
            for line in input_file:
                input = line.strip()
                process_input(input)

    else:
        for input in sys.stdin:
            input = str(input).strip()
            process_input(input)


if __name__ == "__main__":
    # Set up logging to write to a file in the input file directory scenario
    global logger
    logger = setup_logger("root")

    main()
