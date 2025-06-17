import subprocess


def test_task2():
    result = subprocess.run(
        ['python', 'task2/solution.py'], text=True
    )
    assert result.returncode == 0, ('Script failed with stderr: '
                                    f'{result.stderr}')
