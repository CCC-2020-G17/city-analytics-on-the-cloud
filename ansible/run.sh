#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -i playbooks/inventory/inventory.ini --ask-become-pass --tags "servers-init" site.yaml