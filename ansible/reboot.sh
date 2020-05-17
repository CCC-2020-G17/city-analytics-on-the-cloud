#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -i playbooks/inventory/inventory.ini playbooks/reboot.yaml