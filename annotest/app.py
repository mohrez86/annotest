import os
import subprocess
import sys

from annotest import commandline, constant

# from annotest.preparation.fixer_step import fixing_process
from annotest.preparation.trimmer import keepTestableProject
from annotest.project_info.collecter import getProject
from annotest.project_info.project_type import ProjectInfo
from annotest.unittest_engine.generator import generate_tests


def remove_unused_imports():
    test_dir_path_str = constant.testDirPath.absolute().resolve()
    command = [
        "autoflake",
        "--remove-all-unused-imports",
        "-i",
        "-r",
        test_dir_path_str,
    ]
    subprocess.run(command)


def blacken_tests():
    test_dir_path_str = constant.testDirPath.absolute().resolve()
    command = ["black", test_dir_path_str]
    subprocess.run(command)


def generateTests():
    projectDat: ProjectInfo = getProject(constant.projectRoot)
    # fixing_process(projectDat)
    keepTestableProject(projectDat)
    generate_tests(projectDat)
    remove_unused_imports()
    blacken_tests()
    print(f"Test generation finished. Tests are in directory `{constant.testDirPath}`.")


def run():
    commandLineArgs = commandline.parseArgs()
    try:
        os.chdir(commandLineArgs.projectDirectory.absolute())
    except FileNotFoundError as err:
        print(err)
        sys.exit()

    generateTests()
