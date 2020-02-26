def file_loop(array):
    list_of_files_master = []
    for i in array:
        for j in glob.glob(i + '\*'):
            list_of_files_master.append(j)
    return list_of_files_master

def element_add(key, array):
    if key in data.keys():
        array.append(data[key])
        return True
    else:
        array.append('NA')
    return array