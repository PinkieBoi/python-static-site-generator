import os
import shutil
from functions import generate_page


def find_files(directory, files):
    return [file for file in files if os.path.isfile(os.path.join(directory, file))]


def create_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    shutil.copytree("content", "public", ignore=find_files)
    shutil.copytree("static", "public", dirs_exist_ok=True)


def convert_pages():
    # TODO: Change to recursively gen all pages in content dir
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )


def main():
    # root_dir = os.path.abspath(".")
    if not os.path.exists("static"):
        os.mkdir("static")
    create_public()
    convert_pages()


if __name__ == '__main__':
    main()