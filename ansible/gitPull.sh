#!/usr/bin/env bash
. ./openrc.sh; ansible-playbook -i playbooks/inventory/inventory.ini --tags "github" playbooks/test.yaml