# coding=utf-8
import os
import shutil
import wast_builder


base_path = os.path.abspath(os.curdir)
# print(base_path)


'''
需要编译的源文件
'''
source_files = []
source_folder = os.path.join(base_path, r"src")
source_files.append(os.path.join(source_folder, 'algorithm.cpp'))
source_files.append(os.path.join(source_folder, 'any.cpp'))
source_files.append(os.path.join(source_folder, 'bind.cpp'))
source_files.append(os.path.join(source_folder, 'condition_variable.cpp'))
source_files.append(os.path.join(source_folder, 'exception.cpp'))
source_files.append(os.path.join(source_folder, 'functional.cpp'))
source_files.append(os.path.join(source_folder, 'future.cpp'))
source_files.append(os.path.join(source_folder, 'ios.cpp'))
source_files.append(os.path.join(source_folder, 'iostream.cpp'))
source_files.append(os.path.join(source_folder, 'locale.cpp'))
source_files.append(os.path.join(source_folder, 'memory.cpp'))
source_files.append(os.path.join(source_folder, 'mutex.cpp'))
source_files.append(os.path.join(source_folder, 'new.cpp'))
source_files.append(os.path.join(source_folder, 'optional.cpp'))
source_files.append(os.path.join(source_folder, 'regex.cpp'))
source_files.append(os.path.join(source_folder, 'shared_mutex.cpp'))
source_files.append(os.path.join(source_folder, 'stdexcept.cpp'))
source_files.append(os.path.join(source_folder, 'string.cpp'))
source_files.append(os.path.join(source_folder, 'strstream.cpp'))
source_files.append(os.path.join(source_folder, 'system_error.cpp'))
source_files.append(os.path.join(source_folder, 'thread.cpp'))
source_files.append(os.path.join(source_folder, 'typeinfo.cpp'))
source_files.append(os.path.join(source_folder, 'utility.cpp'))
source_files.append(os.path.join(source_folder, 'valarray.cpp'))
source_files.append(os.path.join(source_folder, 'variant.cpp'))
source_files.append(os.path.join(source_folder, 'vector.cpp'))


'''
需要包含的头文件目录
'''
libc_dir = r"E:\Github\libc"
include_foders = []
include_foders.append(os.path.join(base_path, r"include"))
include_foders.append(os.path.join(base_path, r"..\libc\include"))
system_include_foders = []
system_include_foders.append(os.path.join(base_path, r"include"))


'''
输出文件夹
'''
destination_foder = os.path.join(base_path, r"build_bc")
if os.path.exists(destination_foder):
    files = os.listdir(destination_foder)
    for file in files:
        pathname = os.path.join(destination_foder, file)
        if os.path.isdir(pathname):
            shutil.rmtree(pathname)
        else:
            os.remove(pathname)
else:
    os.mkdir(destination_foder)


wast_builder.compile_wast(source_files, include_foders, destination_foder, 'libc++.bc', system_include_foders)
