import subprocess

limit = 100
cmd = "python manage.py test"
proc = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)
counter = 0
isSuccess = False
for bs in iter(proc.stderr.readline, ''):
    line = bs.decode(encoding='utf-8')
    print(line)
    counter += 1
    if line == "" or counter > limit:
        break
    if line.startswith("OK"):
        isSuccess = True

(result, exit_code) = ("Success", 0) if isSuccess else ("Failed", 1)
print(f"::set-output name=result::{result}")
exit(exit_code)
