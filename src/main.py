import os
import shutil
from functions import generate_page


def create_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    shutil.copytree("content", "public", copy_function=generate_page)
    shutil.copytree("static", "public", dirs_exist_ok=True)


def main():
    if not os.path.exists("static"):
        os.mkdir("static")
    create_public()


if __name__ == '__main__':
    main()