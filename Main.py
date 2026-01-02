#Develop in Jupyter environment

import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def roll_num_die(num=3):
    return [random.randint(1, 6) for _ in range(num)]

res_sum_count = [[i + 1, 0] for i in range(2, 18)]
res_count = [[i + 1, 0] for i in range(6)]
res_Diceface = [[i + 1, 0] for i in range(6)]
all_same = 0

NUM_ROLLS = 10000

for _ in range(NUM_ROLLS):
    res = roll_num_die()
    res_sum = sum(res)
    res_sum_count[res_sum - 3][1] += 1
    for j in range(len(res)):
        res_count[res[j] - 1][1] += 1
    for k in range(1, 7):
        if k in res:
            res_Diceface[k - 1][1] += 1
    if len(set(res)) == 1:
        all_same += 1
    percent = (_ + 1) / NUM_ROLLS * 100
    print(f"\r{_ + 1} / {NUM_ROLLS} ({percent:.2f}%)", end="", flush=True)

res_count_df = pd.DataFrame(res_count, columns=["Dice", "count"])
res_Diceface_df = pd.DataFrame(res_Diceface, columns=["DiceFace", "count"])
res_sum_count_df = pd.DataFrame(res_sum_count, columns=["Sum", "count"])
print('\n', res_count_df, '\n', res_Diceface_df, '\n', res_sum_count_df)

res_count_df = res_count_df.set_index('Dice')
res_count_df.plot(kind='bar')
plt.xlabel("Dice Face")
plt.ylabel("Count")
plt.show()

res_Diceface_df = res_Diceface_df.set_index('DiceFace')
res_Diceface_df.plot(kind='bar')
plt.xlabel("Dice Face")
plt.ylabel("Count")
plt.show()

res_sum_count_df = res_sum_count_df.set_index('Sum')
ax = res_sum_count_df.plot(kind='bar', alpha=0.7)

# Reconstruct raw sum data for statistics
sums = []
for s, c in res_sum_count:
    sums.extend([s] * c)

# Mean and standard deviation
mu = np.mean(sums)
sigma = np.std(sums)

# Normal distribution curve
x = np.arange(3, 19)
pdf = norm.pdf(x, mu, sigma)

# Scale PDF to match bar heights
pdf_scaled = pdf * NUM_ROLLS * 1  # bin width = 1

# Overlay curve
ax.plot(
    x - 3,
    pdf_scaled,
    color='red',
    linewidth=2,
    label='Normal Distribution'
)

ax.legend()
plt.xlabel("Sum of Dice")
plt.ylabel("Count")
plt.show()
