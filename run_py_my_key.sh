#!/usr/bin/env bash
until python py_my_key/cli_rpi_access.py; do
	echo "Sleep 2 seconds"
	sleep 2
done

