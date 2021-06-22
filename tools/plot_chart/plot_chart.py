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
ax = df.set_index('query')[df.columns[1:]].plot.bar()

plt.xticks(rotation=45, fontsize=7)
plt.xlabel("query")
plt.tight_layout()
plt.ylim(bottom=0, top=5000)
plt.ylabel("execution time [ms]")

bars = ax.patches
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, f"{yval:.1f}")

# rects = ax.patches # Make some labels.
# labels = ["label%d" % i for i in range(len(rects))]
# for rect, label in zip(rects, labels):
    # height = rect.get_height()
    # ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            # ha='center', va='bottom')


timestamp = str(datetime.now().strftime('%Y_%m_%d_%H%M%S'))
db_names = [get_db_srv_names(c) for c in df.columns[1:]]
names = '-'.join(db_names)
bench_chart_fname = f"{names}-{timestamp}.png"
bench_chart_path = f"{charts_out_dir}/{bench_chart_fname}"
plt.savefig(bench_chart_path)
plt.show()
