"""
GitHub Action core content.

Slight hacky and roundabout approach, but it should be okay for our purposes.

We operate in context with the repository we're performing the action on.
That repository should contain a tree of markdown files that we want to parse.

For each file, we check whether its header yaml exists, and if so, whether it has a `devcontainer` key.
That key should give us subkeys of `repository_url` and `language`.

We then look up the `devcontainer.repository_url` and try to create a docker container from that repository's
`.devcontainer/Dockerfile`.

We then parse the whole markdown file to insert a comment before each line that isn't a code block f the `language`.
That way we preserve line numbers in the case of errors.

We take the resulting file and feed it into the docker container. If the container exits with a 0 status, we're good.
"""

import os
import re
import yaml
import shutil

from const import DEV_CONTAINER_YAML, LANGUAGE, REPOSITORY_URL
from parser import parse_yaml_frontmatter

# Walk the directory and look for markdown files
for root, dirs, files in os.walk("."):
    for file in files:
        # Attempt to open file, skip any that can't be read
        try:
            with open(os.path.join(root, file), "r") as f:
                content = f.read()
        except Exception as e:
            continue
        
        # Parse the yaml front matter
        yaml_fm = parse_yaml_frontmatter(content)
        repository_url = yaml_fm.repository_url
        language = yaml_fm.language
        
        # If we have a repository_url, we can try to build the container
        if repository_url:
            print(f"Building container for {repository_url}")
            # TODO: Build the container
            pass
        
        # If we have a language, we can parse the file
        if language:
            print(f"Parsing {file} for {language}")
            
            # TODO: Parse the file, use a subprocess or a function call?
            pass

            
            
        
        
        
                    
                
