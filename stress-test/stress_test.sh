#!/bin/bash

# cmd='docker-compose exec redis-eurovoc query /queries/07_get_sorted_labels.cypher'
query="${query:-/queries/07_get_sorted_labels.cypher}"
db_container="${db_container:-testredisgraph}"
cmd="docker exec $db_container query $query"
out_dir="${out_dir:-redis_results}"
err_dir="${err_dir:-redis_errors}"
n="${n:-10}"
rm -rf $out_dir $err_dir
mkdir $out_dir $err_dir
seq 1 $n | parallel $cmd \
	\> $out_dir/result-{}.txt 2\> $err_dir/err-{}.txt
