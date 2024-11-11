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
result = nr.run(napalm_cli, commands=["show running-config"])
with open ('./cfg/running_cfg_R22', 'a') as file:
    file.writelines(result["R22"].result["show running-config"])
with open ('./cfg/running_cfg_R21', 'a') as file:
    file.writelines(result["R21"].result["show running-config"])
   # file.writelines(result["R21"][0].result)
#print(result["R22"][0].result["show interfaces"])
#print(result["R21"][0].result["show interfaces"])
