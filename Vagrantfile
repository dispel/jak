# -*- mode: ruby -*-
# vi: set ft=ruby :

$provisionScript = <<SCRIPT
echo Beginning custom provisioning...
sudo su

# Don't expect stdin during provisioning
export DEBIAN_FRONTEND=noninteractive

# Let's install some pythons!
apt-get update
add-apt-repository ppa:fkrull/deadsnakes -y
apt-get update
apt-get install build-essential libssl-dev libffi-dev python-dev python3.5-dev python3-dev -y
apt-get install python3.5 pypy python-pip git -y

# Virtualenvs for quickly switching between python 2 and 3
pip install virtualenvwrapper

# Switch back to vagrant user instead of root
su vagrant

# Add ye olden virtualenvwrapper settings to the .profile and load them in.
# TODO: This is the one thing that is not idempotent...
sed -i "$ a # Virtualenvwrapper settings" /home/vagrant/.profile
sed -i "$ a export WORKON_HOME=/home/vagrant/.virtualenvs" /home/vagrant/.profile
sed -i "$ a export PROJECT_HOME=/home/vagrant/Devel" /home/vagrant/.profile
sed -i "$ a source /usr/local/bin/virtualenvwrapper.sh" /home/vagrant/.profile
source /home/vagrant/.profile

# Pop into the folder where jak lives
cd /vagrant

# Create our two virtualenvironments
# switch between them with "workon py27" for example.
mkvirtualenv py27
mkvirtualenv -p /usr/bin/python3.5 py35

# We should now be in py35 so let's install our dependencies.
pip install --editable .
pip install -r requirements_dev.txt

# py27
workon py27
pip install --editable .
pip install -r requirements_dev.txt

echo Finished custom provisioning!
SCRIPT

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"

  # config.vm.provider "virtualbox" do |vb|
  #   # vb.memory = "2048"
  #   # vb.cpus = 2
  # end

  config.vm.provision "shell", inline: $provisionScript
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
