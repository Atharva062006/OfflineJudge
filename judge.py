import os   
import sys
import shutil
import time

from compiler import compile_code
from runner import run_program
from checker import check_output
from animation import create_progress

# Judge directory location
JUDGE_DIR = os.path.dirname(os.path.abspath(__file__))
EXE_NAME = "a.exe" if sys.platform == "win32" else "a.out"

def detect_lang(path):
    if path.endswith(".cpp"):
        return "cpp"
    if path.endswith(".c"):
        return "c"
    if path.endswith(".java"):
        return "java"
    if path.endswith(".py"):
        return "python"
    return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python judge.py <problem> <source_file>")
        sys.exit(1)
    
    problem, source = sys.argv[1], sys.argv[2]
    
    # Convert source path to absolute (relative to current working directory)
    if not os.path.isabs(source):
        source = os.path.abspath(source)
    
    lang = detect_lang(source)

    if not lang:
        print("Unsupported file type")
        return

    print("Compiling...")
    ok, exe = compile_code(source, lang)
    if not ok:
        print("Compilation Error")
        print(exe)
        return

    print("Compilation Successful")

    tc_dir = os.path.join(JUDGE_DIR, "testcases", problem)

    input_file = os.path.join(tc_dir, "input.txt")
    output_file = os.path.join(tc_dir, "output.txt")

    if not os.path.exists(input_file) or not os.path.exists(output_file):
        print("input.txt or output.txt not found")
        return

    with open(input_file) as f:
        input_lines = f.readlines()

    with open(output_file) as f:
        output_lines = f.readlines()

    if len(input_lines) != len(output_lines):
        print("input.txt and output.txt line count mismatch")
        return

    total = len(input_lines)
    
    progress, total = create_progress(total)
    
    passed = 0
    failed = 0
    tle_count = 0
    rte_count = 0
    wa_count = 0
    failure_details = None

    with progress:
        task = progress.add_task("tests", total=total)

        for i in range(total):
            input_data = input_lines[i]
            expected = output_lines[i]

            if lang == "cpp" or lang == "c":
                cmd = [os.path.join(JUDGE_DIR, "workdir", EXE_NAME)]
            elif lang == "java":
                class_name = os.path.splitext(os.path.basename(source))[0]
                cmd = ["java", "-cp", os.path.join(JUDGE_DIR, "workdir"), class_name]
            elif lang == "python":
                cmd = ["python", exe]
            else:
                cmd = [exe]

            result = run_program(cmd, input_data)

            if result["status"] == "TLE":
                failed += 1
                tle_count += 1
                failure_details = {
                    "index": i + 1,
                    "status": "TLE",
                    "input": input_data.rstrip("\n"),
                    "expected": expected.rstrip("\n"),
                    "got": result["stdout"].rstrip("\n"),
                    "stderr": result["stderr"]
                }
            elif result["status"] == "RTE":
                failed += 1
                rte_count += 1
                failure_details = {
                    "index": i + 1,
                    "status": "RTE",
                    "input": input_data.rstrip("\n"),
                    "expected": expected.rstrip("\n"),
                    "got": result["stdout"].rstrip("\n"),
                    "stderr": result["stderr"]
                }
            elif not check_output(result["stdout"], expected):
                failed += 1
                wa_count += 1
                failure_details = {
                    "index": i + 1,
                    "status": "Wrong Answer",
                    "input": input_data.rstrip("\n"),
                    "expected": expected.rstrip("\n"),
                    "got": result["stdout"].rstrip("\n"),
                    "stderr": result["stderr"]
                }
            else:
                passed += 1

            time.sleep(0.05)
            progress.advance(task)

            if failure_details:
                break
    
    print(f"\n{'='*50}")
    if failed == 0:
        print(f"VERDICT: ACCEPTED")
        print(f"{passed}/{total} testcases passed")
    else:
        print(f"VERDICT: FAILED")
        print(f"{passed}/{total} testcases passed, {failed}/{total} failed")
        if failure_details:
            print(f"Failed at test case #{failure_details['index']}")
            if failure_details["stderr"]:
                print("stderr:")
                print(failure_details["stderr"])
        if wa_count > 0:
            print(f"Total Wrong Answers: {wa_count}")
        if tle_count > 0:
            print(f"Time Limit Exceeded: {tle_count}")
        if rte_count > 0:
            print(f"Runtime Error: {rte_count}")
    print(f"{'='*50}")

    shutil.rmtree(os.path.join(JUDGE_DIR, "workdir"), ignore_errors=True)

if __name__ == "__main__":
    main()