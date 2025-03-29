import subprocess
def compiler_and_run(code):
""execute the dynamically generated python code .""
with open ("temp.py","w") as f
f.write(code)
try :
output=subprocess.run(["python","temp.py"],capture_output=true,text=true)
return output.stdout.strip()
expect f"Execution error : {e}"