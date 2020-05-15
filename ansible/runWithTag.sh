#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -i playbooks/inventory/inventory.ini --ask-become-pass --tags "$1" site.yaml