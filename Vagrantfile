# -*- mode: ruby -*-
# vi: set ft=ruby :

$provisionScript = <<SCRIPT
echo Beginning custom provisioning...

# Don't expect stdin during provisioning
export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get install python3-venv -y

# Pop into the folder where jak lives
cd /vagrant

# One virtual environment on the system Python (3.12 on Ubuntu 24.04).
# CI runs the tests on every other supported version.
python3 -m venv ~/venvs/jak
source ~/venvs/jak/bin/activate

pip install --editable .
pip install -r requirements_dev.txt

echo Finished custom provisioning!
SCRIPT

Vagrant.configure(2) do |config|

  config.vm.box = "bento/ubuntu-24.04"

  # config.vm.provider "virtualbox" do |vb|
  #   # vb.memory = "2048"
  #   # vb.cpus = 2
  # end

  config.vm.provision "shell", inline: $provisionScript, privileged: false
end
