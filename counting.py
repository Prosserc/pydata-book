# load data (common setup)
import json
path = 'ch02/usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]
print(f"loaded {len(records)} records")

# count timezone data without pandas
from collections import Counter
from pprint import pprint
print("\nsummary loaded using collections.Counter...")
top_10_tz = Counter([rec['tz'] for rec in records if 'tz' in rec]).most_common(10)
pprint(top_10_tz)

# count with pandas
from pandas import DataFrame
frame = DataFrame(records)
print('\nsummary loaded using pandas...')
top_10_tz_pd = frame['tz'].value_counts()[:10]
print(top_10_tz_pd)

# plot easily with pandas
from matplotlib import pyplot as plt
top_10_tz_pd.plot(kind='barh', rot=0)
plt.show()


## MORE ANALYSIS WITH PANDAS
import numpy as np
import pandas as pd
cframe = frame[frame.a.notnull()]
os  = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
by_tz_os = cframe.groupby(['tz', os])  # create a group by
agg_counts = by_tz_os.size().unstack().fillna(0)  # unstack to turn back into tabular data
indexer = agg_counts.sum(1).argsort()
cnt_sub = agg_counts.take(indexer)[-10:]
print('\nTop timezones split by windows / non windows users')
print(cnt_sub)
cnt_sub.plot(kind='barh', stacked=True)
plt.show()

normed_subset = cnt_sub.div(cnt_sub.sum(1), axis=0)  # div each val by sum of col 1
normed_subset.plot(kind='barh', stacked=True)
plt.show()


