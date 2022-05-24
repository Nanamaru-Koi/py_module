import os
import glob
import pickle
import numpy as np
import copy
from natsort import natsorted

def readtxt( path,data_form='data' ):
	""" ==  readtxt  ==========
	
	"""
	
	if type(path) == str:


	elif type(path) == list:



	#the variable of path replesent the parent's path
	
	length = []
	time_len = []
	
	folders_top = natsorted(glob.glob(  os.path.join( path, '[0-9]*')   ))
	
	
	indx_start = 0
	indx_end = 0
	counter_base = 0
	
	fig_title = ["0h"]
	
	
	for folder_top in folders_top:
		
		folders_under = natsorted(glob.glob(  os.path.join( folder_top, '[0-9]*')   ))
		
		for data_folder in folders_under:
			files_txt = natsorted(glob.glob(  os.path.join( data_folder, '*txt')   ))
			
			#if txt files in the folder don't exist 
			if len(files_txt) == 0:
				continue
			# reading all the files
			#length : tool length
			#time_len : time for tool length
			#data_np
			
			
			#print("---------------------------")
			#print(data_folder)
			for i,file in enumerate(files_txt):
			
				
				f = open(file,'r')
				f.readline()[:-1]
				length.append( int( f.readline()[:-1] )/10000 )
				f.close()
				data_np = np.loadtxt(file,delimiter=',',skiprows=2)
				
				indx_end += data_np.shape[0]
				
				
				#the first tool length is supposed to 0
				if counter_base == 0:
					time_len.append(0)
					all_data = np.zeros([1000000,data_np.shape[1]+1])
				else:
					###
					time_len.append( time_len[counter_base-1] + data_np.shape[0]*0.25/3600 )
				
				all_data[indx_start:indx_end,1:] = data_np
				#print("S: %d, E: %d" % (indx_start, indx_end ) )
				
				indx_start = indx_end
				
				counter_base += 1

			fig_title.append( str( round(time_len[-1],1) ) + "h" )
	#adjustment of all_data
	logi = all_data[:,4] != 0
	new_all_data = all_data[logi,:]
	#print(new_all_data.shape[0])
	new_all_data[:,0] = np.arange(0,new_all_data.shape[0]) * (0.25/3600)
	
	new_length = np.vstack([np.array(time_len), np.array(length)]).T
	
	return (new_all_data, new_length, fig_title)
	

def readNPY( path ):
	""" ==  readNPY  ==========
	
	"""
	
	folders_top = natsorted(glob.glob(  os.path.join( path, '[0-9]*')   ))
	
	data_list = []
	
	for folder_top in folders_top:
		
		folders_under = natsorted(glob.glob(  os.path.join( folder_top, '[0-9]*')   ))
		
		for data_folder in folders_under:
			files_txt = natsorted(glob.glob(  os.path.join( data_folder, '*npy')   ))
			
			# reading all the files
			#length : tool length
			#time_len : time for tool length
			#data_np
			
			
			#print("---------------------------")
			#print(data_folder)
			for i,file in enumerate(files_txt):

				data = np.load(file)
				indx_sort = [0,0,0]
        
				data_mean = np.mean(data,axis=0)
				z_posi = np.argmin(data_mean)

				
				for j in [2,0,1]:
					indx_sort[j] = int(z_posi)
					
					if z_posi == 2:
						z_posi = 0
					else:
						z_posi += 1
				
				data_list.append( data[:,indx_sort] )
				
	
	return data_list