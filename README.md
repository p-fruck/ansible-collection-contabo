# Ansible Collection - pfruck.contabo

> :warning: I am not affiliated in any way with Contabo

This is an UNOFFICIAL Ansible collection for [contabo.com](https://contabo.com), which is a hosting provider for VPS and dedicated servers.

The goal of this collection is to make management of your server instances more easy and automated using Ansible and the freshly released [Contabo API](https://api.contabo.com/).

## Example playbook:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local
  vars_files:
    - contabo.vault.yml

  tasks:
  - name: Retrieve Bearer API token
    pfruck.contabo.auth:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      username: "{{ username }}"
      password: "{{ password }}"
    register: oauth_response
    no_log: yes

  - name: "Retrieve access token from response"
    set_fact:
      cntb_token: "{{ oauth_response.msg.access_token }}"
    no_log: yes

  - name: Retrieve list of all contabo compute instances
    pfruck.contabo.instance_info:
      api_key: "{{ cntb_token }}"
    register: result

  - name: Print the name of the first compute instance
    debug:
      msg: "{{ result.msg[0].name }}"
```
