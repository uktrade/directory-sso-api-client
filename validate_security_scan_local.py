#!/usr/bin/env python3

import sys
from pathlib import Path

SIGNED_OFF_BY_TRAILER = 'Signed-off-by: DBT pre-commit check'


def main() -> int:
    if len(sys.argv) != 2:
        print('Expected exactly one commit message filename argument.', file=sys.stderr)
        return 1

    commit_msg_path = Path(sys.argv[1])
    if not commit_msg_path.exists():
        print(f'Commit message file not found: {commit_msg_path}', file=sys.stderr)
        return 1

    lines = commit_msg_path.read_text(encoding='utf-8').splitlines()
    filtered_lines = [line for line in lines if not line.startswith('Signed-off-by')]

    output_lines = list(filtered_lines)
    if output_lines and output_lines[-1] != '':
        output_lines.append('')
    output_lines.append(SIGNED_OFF_BY_TRAILER)

    commit_msg_path.write_text('\n'.join(output_lines) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
