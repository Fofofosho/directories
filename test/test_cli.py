import subprocess
import os


def test_cli():
    return_code = subprocess.call(["python3", "directories.py", "-f", "test/input.txt"])

    assert return_code == 0

    # Find the most recent log file in logs directory
    log_files = os.listdir("logs")
    sorted_log_files = sorted(log_files, reverse=True)
    latest_log_file = sorted_log_files[0]

    print(f"Latest log file: {latest_log_file}")

    with (
        open(f"logs/{latest_log_file}", "r") as result_file,
        open("test/expected-output.txt", "r") as expected_output,
    ):
        assert len(result_file.readlines()) == len(expected_output.readlines())

        for result_line, expected_line in zip(result_file, expected_output):
            assert result_line == expected_line
