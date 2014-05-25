from django.conf import settings
import os

import gitlab
from django.conf import settings
from subprocess import call, check_output
import StringIO, pprint

import ftplib
import ftputil




def synchronize_deployment(deployment):

	# initialize the gitlab client
	gitlab_client = gitlab.Gitlab(settings.GITLAB_URL, deployment.creator.settings.gitlab_token)

	# use this for output
	output = StringIO.StringIO()

	success = True


	# check if the repository is already there
	repo_root = deployment.get_repository_root()

	# shortcut to CD in the repository root
	cd = "cd "+repo_root+" && "

	output.write("Starting FTP Sync\n")



	if not os.path.isdir(repo_root):
		# create the repository
		os.makedirs(repo_root)
		output.write("[LOCAL] Creating repository directory in "+repo_root+"\n")

	# check if there is already a git repository

	

	try:
		check_output(cd+"git status", shell=True)
	except:
		# generate one
		gitlab_project = gitlab_client.getproject(deployment.project.gitlab_id)

		# clone stuff
		cmd = "export GIT_SSL_NO_VERIFY=true && git clone "+gitlab_project['ssh_url_to_repo']+" "+repo_root
		#output.write(cmd+"\n")

		output.write("System user: "+os.getusername()) 
		output.write("[GIT] Cloning Repository\n")
		try:
			response = check_output(cmd, shell=True)
			output.write(response.decode("utf-8")+"\n")
		except:
			output.write("[GIT] Cloning failed\n")
			#output.write(response.decode("utf-8")+"\n")
			return(False, output.getvalue())



	# pull
	cmd = cd + "git pull"
	output.write(cmd+"\n")
	res = check_output(cmd, shell=True).decode("utf-8")
	output.write("[GIT] Pulling\n")
	output.write(res+"\n")

	# current revision
	current_revision = check_output(cd +" git rev-parse HEAD", shell=True)
	current_revision = ''.join(current_revision.splitlines())
	current_revision = current_revision.strip()

	
	output.write("[GIT] Current Revision " + current_revision+"\n")

	file_list = []

	# we pulled, let's find the differences
	if deployment.last_revision == "":
		# this is the first commit, list all files

		for dirname, dirnames, filenames in os.walk(repo_root):
			# we don't want files in the .git repository

			if not ".git" in dirname:
				for filename in filenames:
					abs_path = os.path.join(dirname, filename)
					file_list.append(os.path.relpath(abs_path, repo_root))

	else:
		# get diff list
		cmd = cd+"git diff --name-only "+deployment.last_revision+" "+current_revision
		print "\n\n"+cmd+"\n\n"
		res = check_output(cmd, shell=True)

		files = res.split("\n")

		for file_line in files:
			abs_path = os.path.join(repo_root, file_line)
			file_list.append(os.path.relpath(abs_path, repo_root))
		



	
	try:
		host = ftputil.FTPHost(deployment.host, deployment.username, deployment.password)
	except:
		output.write("[FTP] Connection failed")
		return(False, output.getvalue())



	host.chdir(deployment.ftp_home_dir)

	created_dirs = []

	for filename in file_list:

		abs_path = os.path.join(repo_root, filename)

		if os.path.isfile(abs_path):
			dirname = os.path.dirname(filename)
			try:
				if dirname != "":
					if not dirname in created_dirs:
						created_dirs.append(dirname)
						output.write("[FTP] create dir: "+dirname+"\n")
						host.makedirs(dirname)

				output.write("[FTP] upload file: "+filename+"\n")
				host.upload(abs_path, filename)
			except:
				success = False
				output.wirte("----------"+"\n")
				output.write("ERRROR"+"\n")

		elif not os.path.isdir(abs_path):
			output.write("[FTP] deleting file: "+filename+"\n")
			try:
				host.remove(filename)
			except:
				success = False
				output.write("-----------"+"\n")
				output.write("ERROR"+"\n")

	output.write("Synchronization done!\n\n")

	deployment.last_revision = current_revision
	deployment.save()


		

	return (success, str(output.getvalue()))

