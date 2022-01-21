Ansible Role: Auth
=========

This role is executed to define authenticate against the contabo API and define the `ctnb_token` variable.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

```yaml
- hosts: localhost
  vars:
    client_id: <contabo_client_id>
    client_secret: <contabo_client_id>
    username: <contabo_username>
    password: <contabo_password>
  roles:
    - pfruck.contabo.auth
```


License
-------

[GPL-3.0](https://raw.githubusercontent.com/p-fruck/ansible-collection-contabo/main/LICENSE)

Author Information
------------------

This role was created in 2022 by [Philipp Fruck](p-fruck.eu).

#### Maintainer(s)

- [Philipp Fruck](https://github.com/p-fruck)
