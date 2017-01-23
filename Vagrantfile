# -*- mode: ruby -*-
# vi: set ft=ruby :

$provisionScript = <<SCRIPT
echo Beginning custom provisioning...

# Don't expect stdin during provisioning
export DEBIAN_FRONTEND=noninteractive

# Let's install some Snakes!
sudo apt-get update
sudo add-apt-repository ppa:fkrull/deadsnakes -y
sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev -y
sudo apt-get install python3-dev python-dev -y
sudo apt-get install python3.3-dev python3.3 -y
sudo apt-get install python3.4-dev python3.4 -y
sudo apt-get install python3.5-dev -y
sudo apt-get install python3.6-dev python3.6 -y
sudo apt-get install pypy pypy-dev python-pip git -y

# Update pip
sudo pip install --upgrade pip

# Virtualenvs for quickly switching between python 2 and 3
sudo pip install virtualenvwrapper

# Add ye olden virtualenvwrapper settings to the .profile and load them in.
sed -i "$ a # Virtualenvwrapper settings" /home/ubuntu/.profile
sed -i "$ a export WORKON_HOME=/home/ubuntu/.virtualenvs" /home/ubuntu/.profile
sed -i "$ a export PROJECT_HOME=/home/ubuntu/Devel" /home/ubuntu/.profile
sed -i "$ a source /usr/local/bin/virtualenvwrapper.sh" /home/ubuntu/.profile
source /home/ubuntu/.profile

# Pop into the folder where jak lives
cd /vagrant

# Create our two virtualenvironments
# switch between them with "workon py27" for example.
mkvirtualenv py27
mkvirtualenv -p /usr/bin/python3.6 py36
mkvirtualenv -p /usr/bin/pypy pypy

# We should now be in py36 so let's install our dependencies.
pip install --editable .
pip install -r requirements_dev.txt

# py27
workon py27
pip install --editable .
pip install -r requirements_dev.txt

# # PyPy
# workon pypy
# pip install --editable .
# pip install -r requirements_dev.txt

echo Finished custom provisioning!
SCRIPT

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"

  # config.vm.provider "virtualbox" do |vb|
  #   # vb.memory = "2048"
  #   # vb.cpus = 2
  # end

  config.vm.provision "shell", inline: $provisionScript, privileged: false
end

# How the actual box is setup.
# sudo su
# apt-get update
# add-apt-repository ppa:fkrull/deadsnakes
# apt-get update
# apt-get install python2.7 python3.5 pypy
# apt-get install python-pip
# apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev git # for building cryptography among other things.
# Wasn't so hard was it?
