Ansible Role: Reinstall
=========

Reinstall a given Contabo compute instance with the specified image. Use this role carefully, it will wipe your existing installation.

Requirements
------------

You need a Contabo compute instance as well as your [API](https://api.contabo.com) credentials

Role Variables
--------------

| Variable name    | Example value    | Description |
|------------------|------------------|-------------|
| cntb_token       | <YOUR API TOKEN> | Your Contabo Bearer token is required for authentication. |
| cntb_instance_id | 100000000        | ID of the instance to reinstall. |
| cntb_image_name  | ubuntu-20.04     | The name of the image to install. It must match the image name exactly. Therefore `ubuntu-20` is not a valid name, but `ubuntu-20.04-plex` is. |
| cloud_init_file  | ./cloud-init.yml | The path to your [cloud-init [ ]( https://cloud-init.io/) file. |

Dependencies
------------

community.crypto role needs to be installed

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- hosts: localhost
  vars:
    cntb_token: "YOUR_API_TOKEN"
    cntb_instance_id: 100000000
    cntb_image_name: "ubuntu-20.04"
    cloud_init_file: "./cloud-init.yml"
  roles:
    - pfruck.contabo.reinstall
```

License
-------

[GPL-3.0](https://raw.githubusercontent.com/p-fruck/ansible-collection-contabo/main/LICENSE)

Author Information
------------------

This role was created in 2022 by [Philipp Fruck](p-fruck.eu).

#### Maintainer(s)

- [Philipp Fruck](https://github.com/p-fruck)
