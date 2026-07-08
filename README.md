# dynamic-inventories-parser-for-ansible

Simple tool, that parses data from yc and forms an inventory list to automatically detect hosts' needed data.

Now you can see server's ip address and username.

To make this work, do the following steps:

0. You need to have a Yandex account and be regestered in yc, as the shell commmand I'm using is yc.
```bash
yc init
```

1. Place this file in the same folder where you work with Ansible

2. Make file executabele:

```bash
chmod +x inventories.py
```

3. You may need to configure path to your python interpreter yourself

Command:

```bash
ansible-inventory -i inventory.py --list
```
