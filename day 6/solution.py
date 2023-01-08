with open("input.txt", "+r") as file:
    buffer = file.read().rstrip("\n")

for i in range(len(buffer)):
    if len(set(buffer[i : i + 4])) != 4:
        continue
    packet_start_marker_position = i + 4
    break

print(f"First star solution: {packet_start_marker_position}")

for i in range(len(buffer)):
    if len(set(buffer[i : i + 14])) != 14:
        continue
    message_start_marker_position = i + 14
    break

print(f"Second star solution: {message_start_marker_position}")
