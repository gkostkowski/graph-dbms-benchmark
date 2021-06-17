#!/bin/bash
# Script receives two tabular files and merges them
# returns 'polish' csv: numbers contain commas and fields are separated by ';'

sep=$'\t'
out_sep=';'
f1="$1"
f2="$2"

cat \
	<(echo -e "query${sep}${f1}${sep}${f2}") \
	<(LC_ALL=C join -t "$sep" -1 1 -2 1 -o 1.1,1.2,2.2 \
		<(LC_ALL=C sort -t "$sep" -k1,1 "$f1") \
		<(LC_ALL=C sort -t "$sep" -k1,1 "$f2") \
		| sort -t "$sep" -k1,1) \
	| awk -v osep="$out_sep" \
		'BEGIN {FS="\t";OFS=osep} {gsub(/\./, ",", $2); gsub(/\./, ",", $3)} 1' \
	| rs -c';' -C';' -T \
	| sed 's/'"$out_sep"'$//'
