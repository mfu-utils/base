from typing import Optional

from App.helpers import platform


def check_group_for_deleting(_type: str, name: str, build_type: str) -> bool:
    if _type == 'DELETE':
        return True

    rev = name[0] == '!'
    name = name[1:] if rev else name

    if _type == 'PLATFORM':
        if (platform().name == name) and rev:
            return True

        if (platform().name != name) and not rev:
            return True

    if _type == 'BUILD_TYPE':
        if (build_type == name) and rev:
            return True

        if (build_type != name) and not rev:
            return True

    return False


def load_filtered(build_type: str, path: str) -> str:
    with open(path, 'r') as f:
        data = f.read()

    groups = []
    prev_group: Optional[dict] = None
    deleted_lines = []
    selected_lines = []

    lines = data.split('\n')

    for i, line in enumerate(lines):
        if line.strip().startswith("#:"):
            segments = line.strip()[2:].strip().split(':')
            if segments[0] == 'END':
                groups.append({
                    "group_name": segments[1],
                    "name": segments[2] if len(segments) > 2 else None,
                    "pos": i,
                    "type": "end"
                })

            else:
                groups.append({
                    "group_name": segments[0],
                    "name": segments[1] if len(segments) > 1 else None,
                    "pos": i,
                    "type": "start"
                })

    for group in groups:
        if prev_group:
            if prev_group['group_name'] != group['group_name']:
                raise Exception(f"End group type mismatch at pos '{str(prev_group['pos'])}' in {path} ")

            if group['type'] == 'end':
                if check_group_for_deleting(group['group_name'], group['name'], build_type):
                    deleted_lines += list(range(prev_group['pos'], group['pos'] + 1))
                else:
                    deleted_lines += [prev_group['pos'], group['pos']]

                prev_group = None
            else:
                raise Exception(f"Closed group must be `end` type at pos '{str(group['pos'])}' in {path}")

            continue

        if group['type'] == 'end':
            raise Exception(f"Open group must be `start` type at pos '{str(group['pos'])}' in {path}")

        prev_group = group

    for i, line in enumerate(lines):
        if i in deleted_lines:
            # selected_lines.append(f"# {line}")
            continue

        selected_lines.append(line)

    # print(groups)
    # print(deleted_lines)

    return '\n'.join(selected_lines)
