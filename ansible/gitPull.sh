#!/usr/bin/env bash
. ./openrc.sh; ansible-playbook -i playbooks/inventory/inventory.ini --tags "localhostInit, github" --ask-become-pass site.yaml