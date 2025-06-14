import re
import requests

section_mapping = [
    { "filename": "official-resources.md", "title": "Official Resources", "start": r"## Official Resources", "end": r"## Guides & Getting Started" },
    { "filename": "guides-getting-started.md", "title": "Guides & Getting Started", "start": r"## Guides & Getting Started", "end": r"## Maps and Diagnostics" },
    { "filename": "maps-diagnostics.md", "title": "Maps and Diagnostics", "start": r"## Maps and Diagnostics", "end": r"## Server Software" },
    { "filename": "server-software.md", "title": "Server Software", "start": r"## Server Software", "end": r"## Local Software" },
    { "filename": "local-software.md", "title": "Local Software", "start": r"## Local Software", "end": r"## Hacks and Projects" },
    { "filename": "hacks-projects.md", "title": "Hacks and Projects", "start": r"## Hacks and Projects", "end": r"## Hardware Stores" },
    { "filename": "hardware-stores.md", "title": "Hardware Stores", "start": r"## Hardware Stores", "end": r"## Communities" },
]

def fetch_readme():
    url = "https://raw.githubusercontent.com/ShakataGaNai/awesome-meshtastic/main/README.md"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def clean_section(content):
    # Remove variants of the "back to top" link
    content = re.sub(
        r"\*\*\[\s*`?\^.*?back\s+to\s+top.*?\^`?\s*\]\([^)]+\)\*\*", "", content, flags=re.IGNORECASE
    )
    content = re.sub(r"\*\*\^.*?back\s+to\s+top.*?\^\*\*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"\^.*?back\s+to\s+top.*?\^", "", content, flags=re.IGNORECASE)

    # Replace the first markdown heading (##) with a single #
    content = re.sub(r"^##\s+", "# ", content, count=1, flags=re.MULTILINE)

    # Prepend metadata
    front_matter = "---\nhide:\n  - navigation\n  - toc\n---\n\n"
    return front_matter + content.strip()

def extract_and_save_sections(markdown):
    for section in section_mapping:
        start_pattern = re.escape(section["start"])
        end_pattern = re.escape(section["end"])
        regex = rf"({start_pattern})(.*?)(?={end_pattern})"
        match = re.search(regex, markdown, re.DOTALL)
        
        if match:
            section_text = match.group(0)
            cleaned = clean_section(section_text)
            with open(section["filename"], "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"Saved: {section['filename']}")
        else:
            print(f"Section '{section['title']}' not found.")

if __name__ == "__main__":
    try:
        readme_content = fetch_readme()
        extract_and_save_sections(readme_content)
    except Exception as e:
        print(f"Error: {e}")
