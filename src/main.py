import os
import sys
import shutil
from functions import markdown_to_html_nodes, extract_title


def get_basepath():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "/"


def generate_page(from_path, dest_path):
    basepath = get_basepath()
    print(f"Basepath: {basepath}")
    print(f"Generating page from {from_path} to {dest_path} using template.html")
    with open(from_path, "r") as md_file:
        markdown = md_file.read()
    html_node = markdown_to_html_nodes(markdown)
    page_title = extract_title(markdown)
    with open("template.html", "r") as template_file:
        html_template = template_file.read()
    with open(dest_path.rstrip(".md") + ".html", "w") as html_page:
        page_content = html_node.to_html().replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
        new_page = html_template.replace("{{ Title }}", page_title).replace("{{ Content }}", page_content)
        html_page.write(new_page)


def create_docs():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    dest_dir = "docs" + get_basepath()
    shutil.copytree("content", dest_dir, copy_function=generate_page)
    shutil.copytree("static", dest_dir, dirs_exist_ok=True)


def main():
    if not os.path.exists("static"):
        os.mkdir("static")
    create_docs()


if __name__ == '__main__':
    main()