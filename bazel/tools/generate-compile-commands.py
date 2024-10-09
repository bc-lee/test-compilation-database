#!/usr/bin/env python3
__doc__ = """Modify Bazel's compile_commands.json to use project root directory."""

import shlex
import json
import os
import shutil
import sys
import subprocess

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def get_bazel():
  bazel = os.getenv('BAZEL')
  if bazel:
    return bazel

  bazel = shutil.which('bazelisk')
  if bazel:
    return 'bazelisk'
  if shutil.which('bazel'):
    return 'bazel'

  raise RuntimeError('bazel or bazelisk not found')


def rewrite_command(command, original_directory, output_base):
  shell_command = shlex.split(command)
  length = len(shell_command)
  new_command = []
  i = 0
  while True:
    if i >= length:
      break

    item = shell_command[i]
    if item.startswith("-i") or item.startswith("-isystem"):
      path_part = None
      connected = False
      if "=" in item:
        connected = True
        path_part = item.split("=")[1]
      else:
        i += 1
        path_part = shell_command[i]

      # If the path is relative, make it absolute using the original directory and output_base
      if not path_part.startswith("/"):
        directory = original_directory.replace("__OUTPUT_BASE__", output_base)
        path_part = os.path.join(directory, path_part)
      if connected:
        new_command.append(f"{item.split('=')[0]}={path_part}")
      else:
        new_command.append(item)
        new_command.append(path_part)
    else:
      new_command.append(item)
    i += 1
  return shlex.join(new_command)


def main():
  os.chdir(ROOT_DIR)

  cmd = [get_bazel(), 'build', '//:compdb']
  print(f"Running {shlex.join(cmd)}")
  subprocess.run(cmd, check=True)

  original_compile_commands = Path("bazel-bin/compile_commands.json")
  if not original_compile_commands.exists():
    raise RuntimeError(
      "compile_commands.json not generated. Please check the build logs.")

  cmd = [get_bazel(), 'info', 'output_base']
  print(f"Running {shlex.join(cmd)}")
  output_base = subprocess.run(
    cmd, check=True, capture_output=True).stdout.decode('utf-8').strip()

  print("Copying compile_commands.json to the root directory")
  compile_commands = json.loads(original_compile_commands.read_text())
  new_compile_commands = []
  for item in compile_commands:
    directory = item["directory"]
    file = item["file"]
    if directory.startswith("__OUTPUT_BASE__/execroot/_main"):
      file_path = ROOT_DIR / file
      if file_path.exists():
        original_directory = directory
        item["directory"] = directory.replace("__OUTPUT_BASE__/execroot/_main",
                                              str(ROOT_DIR))
        command = item["command"]
        item["command"] = rewrite_command(command, original_directory,
                                          output_base)
      else:
        item["directory"] = directory.replace("__OUTPUT_BASE__", output_base)
    elif "__OUTPUT_BASE__" in directory:
      raise RuntimeError(
        f"Unexpected directory {directory} in compile_commands.json")
    else:
      # Check if the directory exists
      if not os.path.exists(directory):
        raise RuntimeError(f"Directory {directory} does not exist")
    new_compile_commands.append(item)

  try:
    os.remove("compile_commands.json")
  except FileNotFoundError:
    pass
  with open("compile_commands.json", "w") as f:
    json.dump(new_compile_commands, f, indent=2)


if __name__ == '__main__':
  sys.exit(main())
