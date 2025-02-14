import uvicorn
from server import DenoiserApp
import argparse
import subprocess
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--notebook', action='store_true')

    args = parser.parse_args()
    print(f"Running with arguments\n{args}")

    if args.notebook:
        subprocess.call(
            [sys.executable, '-m', 'notebook', '--allow-root', '--port', '8899', '--ip', '0.0.0.0'],
            cwd='/repo')
        exit(0)

    DenoiserApp().create_app().run('0.0.0.0', 8080)