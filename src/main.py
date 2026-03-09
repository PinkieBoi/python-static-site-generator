import os
import shutil


def create_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    shutil.copytree("static", "public")


def main():
    root_dir = os.path.abspath(".")
    if not os.path.exists(root_dir + "/static"):
        os.mkdir(root_dir + "/static")
    create_public()


if __name__ == '__main__':
    main()