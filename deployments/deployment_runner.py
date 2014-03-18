from fabric.api import *

from deployments.models import Deployment

import StringIO


import traceback, sys



def run_deployment_by_id(deployment_id):
    """ Runs the deployment with the given ID
    returns (success, output)
    """

    deployment = Deployment.objects.get(id=deployment_id)

    return run_deployment(deployment)


def run_deployment(deployment):
    """ Runs the employment given by it's instance

    returns (success, output)
    """

    host = deployment.host
    user = deployment.username
    password = deployment.password
    shell_code = deployment.shell_code

    return execute_remote_code(host, user, password, shell_code, deployment)



def execute_remote_code(host_string, user, password, shell_code, deployment):
    """ Executes the remote shell code with the help of fabric"""

    output = StringIO.StringIO()
    success = True

    output.write("Running deployment "+str(deployment)+"\n")

    try:
        with settings(host_string=host_string, user=user, password=password, abort_on_prompts=True):
            lines = shell_code.splitlines()

            for line in lines:


                output.write("$ "+line+"\n")
                res = run(line)
                output.write(res.stdout+"\n"+res.stderr+"\n")
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        # traceback.print_exc(file=output)
        output.write("Exception:" +str(exc_type)+"\n")
        success = False

    return (success, output.getvalue())


def execute_hook(hook):

    should_run = False

    if hook.every_push:
        should_run = True
    else:
        # check if the regex matches
        # TODO
        pass

    output = StringIO.StringIO()
    success = True

    for deployment in hook.deployments.all():

        (s,o) = run_deployment(deployment)

        output.write(o+"\n-----------------------------------------------------------------------------------------\n")

        if not s:
            success = False

    return (success, output.getvalue())








