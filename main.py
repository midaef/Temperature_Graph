
import matplotlib.pyplot as plt
from ezprint import p
import pandas as pd 
import numpy as np 
import random

date = []
tem = np.random.randint(60, size=(7)) - 30
for i in range(1, 8):
	date.append('Feb-' + str(i))

mas = np.arange((5)+2)
df = pd.DataFrame({
	'Temperature' : tem
	}, index = date)


if __name__ == '__main__':
	p(df)
	line_down, = plt.plot(df, label='Temperature change', c='green', lw=3.5, marker='h', mec='red')
	plt.ylim(-30, 30)
	plt.legend(handles=[line_down])
	plt.title('London')
	plt.xlabel('Date')
	plt.ylabel('Temperature')
	plt.show()
	plt.savefig('1.png')
	p('Save graph!')