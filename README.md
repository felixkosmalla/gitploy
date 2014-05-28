# Deployment Hooks

This tool enables you to build your own self-contained versioning and deployment system. Backed by Django it seamlessly integrates with your GitLab installation and allows you to host your repositories and push changes directly to your staging or production servers, either via remote execution of shell scripts or FTP synchronization. Deployment Hooks is inspired by Beanstalk. 


##Installation




###Create system user

	sudo adduser --disabled-login --gecos 'Deployment User' deploy