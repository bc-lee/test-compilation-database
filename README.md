# test-compilation-database

This repository demonstrates various ways to generate a compilation database for a C++ project. It serves as a test project to check compatibility with compilation database tools, such as different Clang tools.

## 1. Generating the compilation database in the `raw` directory

To generate the compilation database in the `raw` directory, simply run `raw/tools/generate_compilation_database.sh`. The output will be placed in the `raw/out` directory.

## 2. Generating the compilation database in the `bazel` directory

In the `bazel` directory, you'll find a simple Bazel project. There are two methods to generate the compilation database:

### 2.1. Running `bazel/tools/generate_compilation_database.py`

This script utilizes [grailbio/bazel-compilation-database](https://github.com/grailbio/bazel-compilation-database) under the hood and adjusts the output paths to be relative to the project's root directory. The `bazel` project is already set up to use the `grailbio/bazel-compilation-database` tool.

### 2.2. Using `kiron1/bazel-compile-commands`

[kiron1/bazel-compile-commands](https://github.com/kiron1/bazel-compile-commands) is a tool that generates a compilation database from Bazel without requiring modifications to the project's BUILD files. Build the tool and run it in the `bazel` directory.
