from fabric.api import *
import fabric.api

from deployments.models import Deployment

import StringIO, pprint


import traceback, sys, json

from ftp_synchronizer import *



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

    if deployment.deployment_type == Deployment.SSH_SCRIPT:
        return execute_remote_code(host, user, password, shell_code, deployment)

    elif deployment.deployment_type == Deployment.FTP_SYNC:
        return synchronize_deployment(deployment)


    



def execute_remote_code(host_string, user, password, shell_code, deployment):
    """ Executes the remote shell code with the help of fabric"""

    output = StringIO.StringIO()
    success = True

    output.write("Running deployment "+str(deployment)+"\n")

    try:
        with fabric.api.settings(host_string=host_string, user=user, password=password, abort_on_prompts=True):
            lines = shell_code.splitlines()

            for line in lines:
                output.write("$ "+line+"\n")
                res = fabric.api.run(line)
                output.write(res.stdout+"\n"+res.stderr+"\n")
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        # traceback.print_exc(file=output)
        output.write("Exception:" +str(exc_type)+" - "+str(exc_obj)+"\n")
        success = False

    return (success, output.getvalue())


def execute_hook(hook, request):

    should_run = False

    output = StringIO.StringIO()

    if hook.every_push:
        should_run = True
    else:
        # check if the regex matches
        
        # get json from post
        # 
        output.write("received payload from gitlab\n\n")
        payload = json.loads(request.body)
        pp = pprint.PrettyPrinter(indent=4, stream=output)
        pp.pprint(payload)


        # debug
        # pp.pprint(payload['commits'])

        for commit in payload['commits']:
            if hook.regex_matches(commit['message']):
                output.write( "Regexp '"+hook.commit_message_regex+"' match on commit:\n")
                pp.pprint(commit)
                should_run = True            

        pass

    # output = StringIO.StringIO()
    success = True
    if should_run:
        
        output.write("Starting deployments...\n")
        for deployment in hook.deployments.all():

            #(s,o) = (True, "")
            (s,o) = run_deployment(deployment)

            # safe execution
            deployment.save_execution(s,o, hook)

            output.write(o+"\n-----------------------------------------------------------------------------------------\n")

            if not s:
                success = False
    else:
        output.write("We did not run \n")



    return (success, output.getvalue())









