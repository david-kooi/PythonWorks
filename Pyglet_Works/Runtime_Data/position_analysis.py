from matplotlib import pyplot as plt
import numpy as np

auto_adj_PATH = 'auto_adj.txt'
no_adj_PATH = 'no_adj.txt'

data_file_PATH ='data_FILE.txt'



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

	## Fill specific data lists
	position_bufferTime_LIST = []
	velocity_bufferTime_LIST = []
	for row in full_ARRAY:
		
		temp = []
		temp.append(row[0]) # Velocity
		temp.append(row[2]) # Buffer Time
		velocity_bufferTime_LIST.append(temp)

		temp = []
		temp.append(row[1]) # Position
		temp.append(row[2]) # Buffer Time
		position_bufferTime_LIST.append(temp)

	position_buffer_DATA = np.array(position_bufferTime_LIST)
	velocity_buffer_DATA = np.array(velocity_bufferTime_LIST)

	## Create position_buffer plot
	f, axes = plt.subplots(2, sharex=True)
	time_points = np.array(range(len(position_buffer_DATA[:, 0])))

	axes[0].set_title('Buffer_Time')
	axes[0].plot(time_points, position_buffer_DATA[:, 0])

	axes[1].set_title('Y_Position')
	axes[1].plot(time_points, position_buffer_DATA[:, 1])

	print time_points
	print position_buffer_DATA

	print 'about to show'
	plt.show()


	#plt.plot(position_buffer_DATA[:,])

#	## Plot auto_adj_data
#	points = np.array(range(auto_adj_data.size))
#
#	plt.plot(points, auto_adj_data)
#	plt.show()
#
#	points = np.array(range(no_adj_data.size))
#
#	plt.plot(points, no_adj_data)
#	plt.show()
