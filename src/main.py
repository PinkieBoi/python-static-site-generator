import os
import shutil
from functions import generate_page


def create_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    shutil.copytree("static", "public")


def convert_pages():
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )


def main():
    root_dir = os.path.abspath(".")
    if not os.path.exists(root_dir + "/static"):
        os.mkdir(root_dir + "/static")
    create_public()
    convert_pages()


if __name__ == '__main__':
    main()