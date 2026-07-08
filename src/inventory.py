#!/opt/homebrew/Cellar/ansible/14.1.0/libexec/bin/python
import json
import subprocess
import yaml


def get_instances():
    '''
    Запускает команду yc compute instance list --format json
    и получает список активных серверов пользователя
    :return: json
    '''
    result = subprocess.run(
        ["yc", "compute", "instance", "list", "--format", "json"],
        text=True,
        check=True,
        capture_output=True,
    )
    return json.loads(result.stdout)

def get_username(name: str):
    '''
    name - название виртуальной машины
    return: имя пользователя
    '''
    result = subprocess.run(
        ["yc", "compute", "instance", "get", name, "--full", "--format", "json"],
        text=True,
        check=True,
        capture_output=True,
    )
    data = json.loads(result.stdout)
    user_data = yaml.safe_load(data['metadata']['user-data'])
    username = user_data['users'][0]['name']
    return username

def build_inventory(instances: dict):
    '''
    Строит динамический инвентарь
    :param instances: устройства
    :return:
    '''
    inventory = {
        "all": {
            "hosts": [],
        },
        "_meta": {
            "hostvars": {}
        }
    }

    for vm in instances:
        name = vm["name"]
        host = vm['network_interfaces'][0]["primary_v4_address"]["one_to_one_nat"]["address"]
        inventory["all"]["hosts"].append(name)
        username = get_username(name)
        inventory["_meta"]["hostvars"][name] = {
            "ansible_host": host,
            "ansible_user": username,
        }
    return inventory


def main():
    '''
    Получает информацию о серверах, билдит динамические инвентари
    '''
    instances = get_instances()
    inventory = build_inventory(instances)
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
