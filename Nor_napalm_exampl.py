from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.plugins.inventory.simple import SimpleInventory
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_utils.plugins.tasks.files import write_file
from nornir_napalm.plugins.tasks import napalm_cli
if __name__ == "__main__":
 InventoryPluginRegister.register("SimpleInventory", SimpleInventory)

 nr = InitNornir(
 runner={
 "plugin": "threaded",
 "options": {
 "num_workers": 30,
 },
 },
 inventory={
 "plugin": "SimpleInventory",
 "options": {
 "host_file": "inventory/hosts.yml",
 "group_file": "inventory/groups.yml",
 "defaults_file": "inventory/defaults.yml"
 }
 },
 dry_run=True,
 )
result = nr.run(napalm_cli, commands=["show version", "show ip interface brief"])
print(result["R22"][0].result["show ip interface brief"])
print(result["R21"][0].result["show ip interface brief"])
print_result(result)
