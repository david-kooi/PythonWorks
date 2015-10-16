from matplotlib import pyplot as plt
import numpy as np

auto_adj_PATH = 'auto_adj.txt'
no_adj_PATH = 'no_adj.txt'

if __name__ == '__main__':
	auto_adj_data = np.genfromtxt(auto_adj_PATH)
	no_adj_data = np.genfromtxt(no_adj_PATH)



	## Plot auto_adj_data
	points = np.array(range(auto_adj_data.size))

	plt.plot(points, auto_adj_data)
	plt.show()

	points = np.array(range(no_adj_data.size))

	plt.plot(points, no_adj_data)
	plt.show()
