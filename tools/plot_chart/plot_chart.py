# Note: generate input with ../format_results/format_to_csv_en.sh script

from datetime import datetime
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt


def get_db_srv_names(path):
    return os.path.splitext(os.path.basename(path))[0]
    

def cut_query_names(name):
    return name.split('/')[-1].split('.')[0]


times_csv_file = sys.argv[1]
charts_out_dir = sys.argv[2]
df = pd.read_csv(times_csv_file)
df['query'] = df['query'].apply(cut_query_names)
df.set_index('query')[[df.columns[1], df.columns[2]]].plot.bar()
plt.xticks(rotation=45)
plt.xlabel("query")
plt.tight_layout()
plt.ylabel("execution time [ms]")

timestamp = str(datetime.now().strftime('%Y_%m_%d_%H%M%S'))
fst_srv_name = get_db_srv_names(df.columns[1])
snd_srv_name = get_db_srv_names(df.columns[2])
bench_chart_fname = f"{fst_srv_name}-{snd_srv_name}-{timestamp}.png"
bench_chart_path = f"{charts_out_dir}/{bench_chart_fname}"
plt.savefig(bench_chart_path)
plt.show()
