#!/bin/bash

res_dir=$1
cat $res_dir/* \
	| awk '{ sum += $0; n++ } END { if (n > 0) print sum / n; }'
