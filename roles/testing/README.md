<!-- BEGIN_ANSIBLE_DOCS -->

# Ansible Role: trippsc2.mssql.testing
Version: 1.2.0

This role installs a testing Microsoft SQL Server.

## Requirements

| Platform | Versions |
| -------- | -------- |
| EL | <ul><li>8</li><li>9</li></ul> |
| Ubuntu | <ul><li>focal</li><li>jammy</li></ul> |

## Dependencies

| Collection |
| ---------- |
| ansible.posix |
| ansible.windows |
| chocolatey.chocolatey |
| community.general |
| community.hashi_vault |
| community.windows |
| trippsc2.hashi_vault |
| trippsc2.windows |

## Role Arguments
|Option|Description|Type|Required|Choices|Default|
|---|---|---|---|---|---|
| dc_inventory_name | <p>The Ansible inventory name of the test domain controller.</p> | str | no |  | dc |


## License
MIT

## Author and Project Information
Jim Tarpley
<!-- END_ANSIBLE_DOCS -->
