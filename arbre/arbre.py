"""This module provides Arbre main module."""

import os
import sys
import pathlib
from dataclasses import dataclass
from enum import Enum
from colorama import Fore, Back, Style

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

class EntryType(Enum):
    BRANCH = 0
    FILE = 1
    FOLDER = 2
    MARKDOWN = 3


@dataclass
class Entry:
    type: EntryType
    text: str = ''
    prefix: str = ''
    connector: str = ''# todo: could make Enum


class _TreeGenerator:
    def __init__(self, root_dir, dir_only=False, show_hidden=False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._show_hidden = show_hidden
        self._tree = []

    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(
            Entry(
                text=f"{self._root_dir}{os.sep}",
                type=EntryType.FOLDER,
            )
        )
        self._tree.append(
            Entry(
                text=PIPE,
                type=EntryType.BRANCH,
            )
        )

    def _tree_body(self, directory, prefix=""):
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:

                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        if not self._show_hidden:
            entries = [entry for entry in entries
                       if not entry.name.startswith(".")]
        return entries



    def _add_directory(self,
                       directory,
                       index,
                       entries_count,
                       prefix, connector):
        self._tree.append(
            Entry(
                # text=f"{prefix}{connector} {directory.name}{os.sep}",
                text=f"{directory.name}{os.sep}",
                type=EntryType.FOLDER,
                prefix=prefix,
                connector=connector
            )
        )
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(
            Entry(
                type=EntryType.BRANCH,
                prefix=prefix.rstrip(),
            )
        )


    def _add_file(self, file, prefix, connector):
        # self._tree.append(f"{prefix}{connector} {file.name}")
        self._tree.append(
            Entry(
                type=EntryType.FILE,
                text=file.name,
                prefix=prefix,
                connector=connector,
            )
        )



class DirectoryTree:
    def __init__(
        self,
        root_dir,
        dir_only=False,
        output_file=sys.stdout,
        show_hidden=False,
    ):
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only, show_hidden)

    def generate(self):
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            # Wrap the tree in a markdown code block
            # TODO: use collections.deque and .appendleft()
            tree.insert(0,
                Entry(
                    type=EntryType.MARKDOWN,
                    text="```"
                )
            )
            tree.append(
                Entry(
                    type=EntryType.MARKDOWN,
                    text="```"
                )
            )
            self._output_file = open(
                self._output_file, mode="w", encoding="UTF-8"
            )
        with self._output_file as stream:
            for entry in tree:
                color_prefix = ''
                if entry.type == EntryType.FOLDER:
                    color_prefix = Fore.BLUE
                text = f"{entry.prefix}{entry.connector}"
                if len(text) > 1 and len(entry.text) > 1:
                    text = f"{text} "
                text = f"{text}{color_prefix}{entry.text}{Style.RESET_ALL}"
                print(f"{text}", file=stream)
