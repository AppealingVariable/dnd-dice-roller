import subprocess
from pathlib import Path

def main():
    app_path = Path.cwd()
    run_command = f'''cmd /k "cd /d {Path.cwd()}/.venv/Scripts/ & activate & cd /d {app_path} & python DiceRoller.pyw'''
    subprocess.Popen(run_command, shell=True)
main()