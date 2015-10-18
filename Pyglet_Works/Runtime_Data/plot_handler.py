from matplotlib import pyplot as plt
import numpy as np

auto_adj_PATH = 'auto_adj.txt'
no_adj_PATH = 'no_adj.txt'

data_file_PATH ='data_FILE.txt'



		  ## Data Format ##
# Velocity | Buffer Time | Position #

def getDataList(f):
	count = 0
	time_point = []
	data_range = []
	for line in f:
		if count > 2:
			data_range.append(time_point)
			time_point = []
			count = 0

		dp = line.split('_')[1]
		time_point.append(dp.split('\n')[0])
		count += 1
	return data_range


if __name__ == '__main__':

	## Open Data File
	f = open(data_file_PATH, 'r')
	#data_array = np.fromfile(f)

	## Parse Data
	data_LIST = getDataList(f)
	full_ARRAY = np.array(data_LIST)

	## Create position_buffer plot
	f, axes = plt.subplots(2, sharex=True)
	time_points = np.array(range(len(full_ARRAY[:, 0])))

		  	  ## Data Format ##
	# Velocity | Buffer Time | Position #
	axes[0].set_title('Buffer_Time')
	axes[0].plot(time_points, full_ARRAY[:, 1])

	axes[1].set_title('Y_Position')
	axes[1].plot(time_points, full_ARRAY[:, 2])
	
	plt.show()

	#


	## Create velocity_buffer plot
	f, axes = plt.subplots(2, sharex=True)
	axes[0].set_title('Buffer_Time')
	axes[0].plot(time_points, full_ARRAY[:, 1])

	axes[1].set_title('Velocity')
	axes[1].plot(time_points, full_ARRAY[:, 0])

	plt.show()

#	plt.plot(points, no_adj_data)
#	plt.show()
