"""This module provides the Arbre CLI."""
# cli.py

import argparse
import pathlib
import sys
from colorama import init as colorama_init
from colorama import Fore

from . import __version__
from .arbre import DirectoryTree

def main():
    colorama_init(autoreset=True)
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print(Fore.RED + "The specified root directory doesn't exist")
        sys.exit()
    tree = DirectoryTree(
        root_dir,
        dir_only=args.dir_only,
        output_file=args.output_file,
        show_hidden=args.all,
    )
    tree.generate()

def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="arbre",
        description="Arbre, a directory tree generator",
        epilog="Thanks for using arbre!",
    )
    parser.version = f"Arbre v{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        help="Generate a full directory tree starting at ROOT_DIR",
    )
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a directory-only tree",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        help="Generate a full directory tree and save it to a file",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Show all files (including hidden ones)",
    )
    return parser.parse_args()

