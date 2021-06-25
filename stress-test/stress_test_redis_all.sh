#!/bin/bash

N="${N:-12}"
DB_CONTAINER=testredisgraph
avg_redis_out="avg-times-redis-${N}.tsv"
rm -f "$avg_redis_out"

QUERY=/queries/01_count_relationships.cypher
	query=$QUERY \
	n=$N \
	db_container=$DB_CONTAINER \
	out_dir=redis_results_q01 \
	err_dir=redis_errors_q01 \
	./stress_test.sh
	

avg_time=$(./calc_avg_time.sh redis_results_q01)
echo -e "$QUERY\t$avg_time" >> "$avg_redis_out"

QUERY=/queries/02_count_context_nodes.cypher
	query=$QUERY \
	n=$N \
	db_container=$DB_CONTAINER \
	out_dir=redis_results_q02 \
	err_dir=redis_errors_q02 \
	./stress_test.sh

avg_time=$(./calc_avg_time.sh redis_results_q02)
echo -e "$QUERY\t$avg_time" >> "$avg_redis_out"

QUERY=/queries/03_substring_check_simple.cypher
	query=$QUERY \
	n=$N \
	db_container=$DB_CONTAINER \
	out_dir=redis_results_q03 \
	err_dir=redis_errors_q03 \
	./stress_test.sh

avg_time=$(./calc_avg_time.sh redis_results_q03)
echo -e "$QUERY\t$avg_time" >> "$avg_redis_out"

QUERY=/queries/04_substring_check_complex.cypher
	query=$QUERY \
	n=$N \
	db_container=$DB_CONTAINER \
	out_dir=redis_results_q04 \
	err_dir=redis_errors_q04 \
	./stress_test.sh

avg_time=$(./calc_avg_time.sh redis_results_q04)
echo -e "$QUERY\t$avg_time" >> "$avg_redis_out"

QUERY=/queries/05_labels_equivalence.cypher
	query=$QUERY \
	n=$N \
	db_container=$DB_CONTAINER \
	out_dir=redis_results_q05 \
	err_dir=redis_errors_q05 \
	./stress_test.sh

avg_time=$(./calc_avg_time.sh redis_results_q05)
echo -e "$QUERY\t$avg_time" >> "$avg_redis_out"

QUERY=/queries/06a_count_triangles.cypher
	query=$QUERY \
	n=$N \
	db_container=$DB_CONTAINER \
	out_dir=redis_results_q06a \
	err_dir=redis_errors_q06a \
	./stress_test.sh

avg_time=$(./calc_avg_time.sh redis_results_q06a)
echo -e "$QUERY\t$avg_time" >> "$avg_redis_out"

QUERY=/queries/07_get_sorted_labels.cypher
	query=$QUERY \
	n=$N \
	db_container=$DB_CONTAINER \
	out_dir=redis_results_q07 \
	err_dir=redis_errors_q07 \
	./stress_test.sh

avg_time=$(./calc_avg_time.sh redis_results_q07)
echo -e "$QUERY\t$avg_time" >> "$avg_redis_out"

echo "Average execution times stored in $avg_redis_out"
