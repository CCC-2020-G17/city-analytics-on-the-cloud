#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -i inventory/inventory.ini --ask-become-pass all-in-one.yaml