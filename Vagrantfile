# -*- mode: ruby -*-
# vi: set ft=ruby :

$provisionScript = <<SCRIPT
echo Beginning custom provisioning...

# Don't expect stdin during provisioning
export DEBIAN_FRONTEND=noninteractive

# Let's install some Snakes!
sudo apt-get update
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get install build-essential libssl-dev libffi-dev -y
# sudo apt-get install python-pip git -y

# Update pip
# sudo pip install --upgrade pip

# Install all the snakes. (3.8 is already in Ubuntu 20 (Focal))
sudo apt install python3.8-venv python3.8-dev python3.9 python3.9-venv python3.9-dev python3.7 python3.7-dev python3.7-venv python3.6 python3.6-dev python3.6-venv pypy3 pypy3-dev -y

# Pop into the folder where jak lives
cd /vagrant

# Virtual environments for python 3.9 and 3.8
# You can use similar commands if you want to test other versions or pypy.
python3.9 -m venv ~/venvs/py39
python3.8 -m venv ~/venvs/py38
pypy3 -m venv ~/venvs/pypy3

# Activate 3.9 virtualenv
source ~/venvs/py39/bin/activate

# We should now be in py39 so let's install our dependencies.
pip install --editable .
pip install -r requirements_dev.txt

echo Finished custom provisioning!
SCRIPT

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/focal64"

  # config.vm.provider "virtualbox" do |vb|
  #   # vb.memory = "2048"
  #   # vb.cpus = 2
  # end

  config.vm.provision "shell", inline: $provisionScript, privileged: false
end
