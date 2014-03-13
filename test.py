from fabric.api import *

import StringIO

print "hello"
output = ""

output = StringIO.StringIO()



def my_run(cmd):


    output.write("$ "+cmd+"\n")
    a = run(cmd, pty=False)
    output.write(a.stdout+"\n")


    
    return a



def test():
    print "test"
    
    with settings(host_string="git.climbtrack.com", user="dummy", password="test123",abort_on_prompts=True):
        print("Executing on %(host_string)s as %(user)s" % env)
        
        my_run("uname -a")
        my_run("echo \"test\"")
        my_run ("pwd")
        my_run("cd test \n pwd")

        
    
#if __name__ == "main":
test()


print output.getvalue()