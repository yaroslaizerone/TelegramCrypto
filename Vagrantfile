# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
    config.vm.box = "generic/ubuntu2204"
    config.vm.synced_folder ".", "/vagrant", disabled: true
    config.vm.synced_folder ".", "/home/vagrant/calldb"
    config.vm.network :forwarded_port, host: 8000, guest: 8000
    config.vm.network "private_network", ip: "192.168.33.10"
    config.vm.network "forwarded_port", guest: 5555, host: 5555
    config.vm.provision "shell" do |s|
	    s.path = "./provision/setup.sh"
	end
	config.vm.provision "shell", run: "always",
    inline: "systemctl start celery.service celeryflower.service"
end