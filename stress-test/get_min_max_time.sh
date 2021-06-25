#!/bin/bash

paste -d, \
	<(echo "$1") \
	<(cat $1/* | sort -rn | tail -n 1) \
	<(cat $1/* | sort -rn | head -n 1)
