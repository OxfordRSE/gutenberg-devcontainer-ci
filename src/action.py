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

# Walk the directory and look for markdown files
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md"):
            with open(os.path.join(root, file), "r") as f:
                content = f.read()
            yaml_match = re.search(r"^---\n([\s\S]*?)\n---", content)
            if yaml_match:
                yaml_block = yaml.safe_load(yaml_match.group(1))
                if yaml_block.get("devcontainer"):
                    devcontainer = yaml_block["devcontainer"]
                    repository_url = devcontainer["repository_url"]
                    language = devcontainer["language"]
                    if repository_url is not None and language is not None:
                        print(f"Found devcontainer in {file}: {repository_url} ({language})")
                    elif repository_url is None:
                        print(f"Found devcontainer in {file}, but no repository_url")
