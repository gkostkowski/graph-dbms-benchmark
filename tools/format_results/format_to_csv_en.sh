#!/bin/bash
# Script receives two tabular files and merges them

sep=$'\t'
out_sep=','
f1="$1"
f2="$2"

cat \
	<(echo -e "query${sep}${f1}${sep}${f2}") \
	<(LC_ALL=C join -t "$sep" -1 1 -2 1 -o 1.1,1.2,2.2 \
		<(LC_ALL=C sort -t "$sep" -k1,1 "$f1") \
		<(LC_ALL=C sort -t "$sep" -k1,1 "$f2") \
		| sort -t "$sep" -k1,1) \
	| awk -v osep="$out_sep" \
		'BEGIN {FS="\t";OFS=osep} {$1=$1} 1'
		# \
	# | rs -c, -C, -T \
	# | sed 's/'"$out_sep"'$//'

# transpose 
# | rs -c';' -C';' -T
# | rs -c"$out_sep" -C"$out_sep" -T \