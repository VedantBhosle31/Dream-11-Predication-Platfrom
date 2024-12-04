import concurrent.futures
import subprocess
import os

scripts = [
    ("batter.py", "male_t20"),
    ("bowler.py", "male_t20"),
    ("fielder.py", "male_t20"),
    ("matchups.py", "male_t20"),
    ("batter.py", "male_others"),
    ("bowler.py", "male_others"),
    ("fielder.py", "male_others"),
    ("matchups.py", "male_others"),
    ("batter.py", "female"),
    ("bowler.py", "female"),
    ("fielder.py", "female"),
    ("matchups.py", "female"),
]


def run_script_with_logging(script_and_arg):
    script_name, argument = script_and_arg

    log_location = os.path.join("data_processing", "logs")
    os.makedirs(log_location, exist_ok=True)
    log_file = os.path.join(log_location, f"{script_name}_{argument}.log")

    with open(log_file, "a") as log:
        try:
            subprocess.run(
                [
                    "python",
                    os.path.join("data_processing", "generators", script_name),
                    argument,
                ],
                stdout=log,
                stderr=log,
                check=True,
            )
            log.write(
                f"\n{script_name} finished successfully with argument '{argument}'.\n"
            )
        except subprocess.CalledProcessError as e:
            log.write(
                f"\nError occurred while running {script_name} with argument '{argument}': {e}\n"
            )


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(run_script_with_logging, scripts)
