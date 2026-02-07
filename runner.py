import subprocess
from config import TIME_LIMIT

def run_program(cmd, input_data):
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIME_LIMIT,
            text=True
        )
        return {
            "status": "OK" if result.returncode == 0 else "RTE",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "TLE",
            "stdout": "",
            "stderr": ""
        }