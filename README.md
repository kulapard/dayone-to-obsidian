# Day One to Obsidian Converter

[![Build Status](https://github.com/kulapard/dayone-to-obsidian/actions/workflows/ci.yml/badge.svg)](https://github.com/kulapard/dayone-to-obsidian/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/kulapard/dayone-to-obsidian/graph/badge.svg?token=Y5EJBF1F25)](https://codecov.io/github/kulapard/dayone-to-obsidian)
[![PyPI - Version](https://img.shields.io/pypi/v/dayone-to-obsidian?color=%2334D058&label=pypi%20package)](https://pypi.org/project/dayone-to-obsidian)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dayone-to-obsidian)
---

Convert your [Day One](https://dayoneapp.com/) journal entries into Markdown files
compatible with [Obsidian](https://obsidian.md).

## Features

- **Complete Data Migration**: Transfers all text, images, and metadata (including creation dates) from Day One entries.
- **Markdown Formatting**: Converts Day One entries into Markdown format, making them compatible with Obsidian and other
  Markdown editors.
- **Tag Support**: Migrates all tags from Day One, allowing for easy categorization and search within Obsidian.
- **Image Embedding**: Automatically transfers and embeds any images from Day One entries into the Markdown files.

## Prerequisites

Before using `dayone-to-obsidian`, ensure you have the following:

- Python 3.10 or higher installed on your machine.
- Your Day One journal exported in JSON format.
- Obsidian installed if you wish to immediately start using your migrated files in Obsidian.

## Installation

```bash
pip install dayone-to-obsidian
```

## Usage

Follow these steps for conversion:

1. **Prepare Your Day One Export**:
   Export your Day One journal entries to a JSON file or directory containing multiple JSON files following the
   [manual](https://dayoneapp.com/guides/tips-and-tutorials/exporting-entries).

2. **Run the Conversion**:
   Open a terminal or command prompt and execute the
   CLI with the appropriate options.
   The command structure is as follows:

   ```bash
   dayone-to-obsidian run --json /path/to/your/dayone_export.json --target /path/to/target_directory [--force] [--tag-prefix=prefix] [--tag=tag1] [--tag=tag2]
   ```

    - `--json`: Path to your Day One export JSON file or directory.
      If not specified, it defaults to the current directory.
    - `--target`: Path to the directory where converted Markdown files will be saved.
      By default, a new folder is created in the current directory.
    - `--force`: Force the overwriting of existing journal folder.
    - `--tag-prefix`: Prefix for tags, allowing customization of how tags are formatted in the converted files.
    - `--tag`: Additional tag(s) to add to all entries. This option can be repeated to include multiple tags.
    - `--help`: Display the help message.

   Example command:

   ```bash
   dayone-to-obsidian run --json ./DayOneExport/Journal.json --target ./ObsidianNotes --tag-prefix=DayOne/ --tag=Imported --tag=Journal
   ```

   This command specifies a Day One JSON export file, sets the target directory for the converted Markdown files, adds a
   prefix to all tags, and includes additional tags for each entry.

3. **Import to Obsidian**:
   Once the conversion process is complete, manually move the generated Markdown files to your Obsidian vault directory.

## Support

If you encounter any issues or have suggestions for improvements, please open an issue in this GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
