import argparse
import re
from typing import List
from dataclasses import dataclass

import yaml

from const import DEV_CONTAINER_YAML, LANGUAGE, REPOSITORY_URL

@dataclass
class YamlFrontMatter:
    language: str
    repository_url: str


def parse_yaml_frontmatter(content: str) -> YamlFrontMatter:
    # TODO: What do we want the default to be here?
    yaml_fm = YamlFrontMatter(language="python", repository_url="")
    
    # Regex to match the yaml front matter
    yaml_match = re.search(r"^---\n([\s\S]*?)\n---", content)
    
    # If the yaml front matter exists, parse it and return the codeblock_label
    if yaml_match:
        yaml_block = yaml.safe_load(yaml_match.group(1))
        if DEV_CONTAINER_YAML in yaml_block:
            devcontainer = yaml_block[DEV_CONTAINER_YAML]
            if LANGUAGE in devcontainer:
                yaml_fm.language = devcontainer[LANGUAGE]
            if REPOSITORY_URL in devcontainer:
                yaml_fm.repository_url = devcontainer[REPOSITORY_URL]
    
    # If the yaml front matter doesn't exist, return "python"
    return yaml_fm

def get_codeblock_label(fn: str) -> str:
    # Read the file and extract the yaml front matter
    with open(fn, 'r') as f:   
        content = f.read()
    yaml_frontmatter = parse_yaml_frontmatter(content)
    return yaml_frontmatter.language

def parse_markdown(fn: str, code_block_label: str) -> List[str]:
    """ 
    Read the file and comment out everything except the code blocks matching
    the `code_block_label` provided.
    """
    # Read the file contents
    with open(fn, 'r') as f:
        content = f.readlines()

    test_content = []
    in_block = False

    # Iterate through the lines of the file and comment out every line not in a 
    # code block with the correct label
    for line in content:
        test_content.append("#"+line)
        if f"``` {code_block_label}" in line:
            in_block = True
        elif in_block:
            if "```" in line:
                in_block = False
            else:
                test_content.pop()
                test_content.append(line)
    
    # Return the altered file content as a list of lines
    return test_content

def write_test_content(fn: str, new_content: List[str]) -> None:
    with open(fn, 'w') as f:
        f.writelines(new_content)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse a markdown file to leave the code blocks executable"
    )
    parser.add_argument("filename", type=str, 
                        help="The filename of the markdown file to parse")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="The filename to write the parsed markdown to")
    parser.add_argument("-l", "--label", type=str, default="python",
                        help="The code block label to uncomment")
    args = parser.parse_args()
    
    # If no label is provided, try to extract it from the yaml front matter
    if not args.label:
        code_block_label = parse_yaml_frontmatter(args.filename)
    else:
        code_block_label = args.label    
    print(f"Parsing markdown file:{args.filename} for executable "
          f"{code_block_label} code blocks.")
    test_content = parse_markdown(args.filename, code_block_label)
    
    # If an output file is provided, write the parsed markdown to that file
    if args.output:
        write_test_content(args.output, test_content)
        print(f"Successfully wrote parsed markdown to {args.output}")
    # Otherwise, print the parsed markdown to the console
    else:
        print("Parsed markdown:")
        print("".join(test_content))
