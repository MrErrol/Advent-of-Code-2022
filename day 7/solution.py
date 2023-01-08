from typing import List

with open("input.txt", "+r") as file:
    terminal_lines = [line.rstrip("\n") for line in file.readlines()]


def is_command(line: str) -> bool:
    return len(line) and line[0] == "$"


def get_list_output(lines: List[str]) -> List[str]:
    for count, line in enumerate(lines):
        if is_command(line):
            return lines[:count]
    return lines


def get_command_type(line: str) -> str:
    return line.split(" ")[1]


def get_local_file_system(full_system: dict, path: List[str]) -> dict:
    local_system = full_system
    for folder in path:
        local_system = local_system[folder]
    return local_system


def update_files(local_system: dict, lines: List[str]):
    for output in lines:
        word_1, name = output.split(" ")
        if name in local_system.keys():
            continue
        if word_1 == "dir":
            local_system[name] = {}
        else:
            local_system[name] = int(word_1)


def is_directory(obj) -> bool:
    return isinstance(obj, dict)


def get_directory_size(directory: dict):
    size = 0
    for obj in directory.values():
        if is_directory(obj):
            size += get_directory_size(obj)
        else:
            size += obj
    return size


def get_directories(directory: dict) -> List[dict]:
    directories = [directory]
    for obj in directory.values():
        if is_directory(obj):
            directories += get_directories(obj)
    return directories


# create filesystem structure
file_system = {}
current_path = []
lines = terminal_lines[:]
while True:
    if not lines:
        break
    line = lines[0]
    lines = lines[1:]
    if not is_command(line):
        assert False  # something went wrong

    command_type = get_command_type(line)

    if command_type == "cd":
        target_dir = line.split(" ")[-1]
        if target_dir == "/":
            current_path = []
        elif target_dir == "..":
            current_path = current_path[:-1]
        else:
            current_path.append(target_dir)

    if command_type == "ls":
        list_output = get_list_output(lines)
        lines = lines[len(list_output) :]
        local_dict = get_local_file_system(file_system, path=current_path)
        update_files(local_dict, list_output)

# get directories sizes
directories = get_directories(file_system)
sizes = [get_directory_size(dir) for dir in directories]
solution_1 = sum(size for size in sizes if size <= 100_000)

print(f"First star solution: {solution_1}")

total_size = 70_000_000
update_require = 30_000_000
total_occupied = get_directory_size(file_system)
current_free = total_size - total_occupied
we_need = update_require - current_free

solution_2 = min([size for size in sizes if size >= we_need])

print(f"Second star solution: {solution_2}")
