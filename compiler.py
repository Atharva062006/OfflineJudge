import subprocess
import os
import shutil
import sys

# Judge directory location
JUDGE_DIR = os.path.dirname(os.path.abspath(__file__))

def compile_code(source_path, lang):
    workdir = os.path.join(JUDGE_DIR, "workdir")
    os.makedirs(workdir, exist_ok=True)

    # Use .exe on Windows, .out on Unix
    exe_name = "a.exe" if sys.platform == "win32" else "a.out"
    exe_path = os.path.join(workdir, exe_name)

    if lang == "cpp":
        cmd = ["g++", source_path, "-O2", "-std=c++17", "-o", exe_path]

    elif lang == "c":
        cmd = ["gcc", source_path, "-O2", "-std=c99", "-o", exe_path]

    elif lang == "java":
        shutil.copy(source_path, workdir)
        cmd = ["javac", os.path.join(workdir, os.path.basename(source_path))]
        exe_path = None

    else:
        return False, "Unsupported language"

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        return False, result.stderr

    return True, exe_path