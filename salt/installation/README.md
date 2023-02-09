# 

# Salt installation on Nodegrid OS

Salt can be installed on Nodegrid by the default 'admin' user.

Download the repository as a zip or use the git clone command.

## Downloading the zip file
- Download this repository as zip file
- Connect to Nodegrid the WebUI as a admin user
- Open the File Manager and navigate to admin_group
- Upload the downloaded file `zpe.nodegrid_examples-main.zip` into the folder
- Close the File Manager window
- Open a Console connection to Nodegrid
- Access the shell as an admin user using the `shell` command
- Navigate to `/var/local/file_manager/admin_group/` 
```shell script
cd /var/local/file_manager/admin_group/
```
- Extract the zip file with
```shell script
mv zpe.nodegrid_examples-main.zip zpe.nodegrid_examples.zip
unzip zpe.nodegrid_examples.zip
```

## Using git clone command
- Connect to the Nodegrid WebUI as a admin user
- Open the Console
- Access the shell as an admin user using the `shell` command
- Navigate to `/var/local/file_manager/admin_group/` 
```shell script
cd /var/local/file_manager/admin_group/
```
- Clone the repository
```shell script
git clone https://github.com/ZPESystems/zpe.nodegrid_examples.git
```

## Install on Nodegrid

```shell script
shell
cd /var/local/file_manager/admin_group/
```
- Extract the zip file with
```shell script
unzip zpe.nodegrid_examples/salt/installation/ipks/saltstack_IPKs.zip
```
- Install on IPKs on Nodegrid
```shell script
sudo mount -o remount,rw /
cd saltstack_IPKs
sudo opkg install *.ipk
```

Done, now follow the instructions in this section: [Nodegrid Proxy Module Configuration](../README.md#nodegrid-proxy-module-configuration)

# Salt installation on Ubuntu
To use this Nodegrid module you need two Ubuntu hosts to set up salt-master and salt-proxy accordingly.

1. For the ubuntu MASTER instance, connect to SSH and execute:
```shell script
sudo apt-get install salt-master
sudo systemctl stop salt-master
```

2. For the ubuntu PROXY instance, connect to SSH and execute:
```shell script
sudo apt-get install salt-minion
sudo systemctl stop salt-minion
```

Done, now follow the instructions in this section: [Nodegrid Proxy Module Configuration](../README.md#nodegrid-proxy-module-configuration)
