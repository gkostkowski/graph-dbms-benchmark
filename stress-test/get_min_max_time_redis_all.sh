#!/bin/bash

ls -1d redis_results_q* | xargs -I {} ./get_min_max_time.sh {}
