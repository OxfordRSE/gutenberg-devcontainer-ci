# gutenberg-devcontainer-ci Action
GitHub Action for validating the code blocks in Gutenberg course material

## Usage

```
name: Check code blocks

on:
  push:
    paths:
      - '**/*.md'
  pull_request:
    paths:
      - '**/*.md'

jobs:
  check-code-blocks:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Run Code block check
        uses: oxfordrse/gutenberg-devcontainer-ci@main
```

## Details

The action will look through all files in the repository for ones with a YAML header specifying:
```yaml
dev_container:
    repository_url: "foobar"
    language: "code block language name"
```

For each markdown file that specifies a language and repository, the action will:
- Try to create a container from the specified repository 
- Make a copy of the markdown file with all lines that aren't part of a code block with the specified language commented out
- Try to run that file in the container

If the code block runs successfully, the action will pass. If there are any errors, the action will fail with the error message.
The line numbers in the error message will correspond to the line numbers in the markdown file.

## Language specification

The language specified in the YAML header should be the name of the language as it would be specified in a code block in markdown.
For example, the language name for a python code block would be `python`.

The code will check for code blocks (fenced with triple backticks) with the specified language name.

## Inputs and outputs

The job has no inputs or outputs. 
If it encounters errors it will fail with the appropriate line number in the error message.
