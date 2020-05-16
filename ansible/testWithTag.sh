#!/usr/bin/env bash
. ./openrc.sh; ansible-playbook -i playbooks/inventory/inventory.ini --tags "$1" playbooks/test.yaml