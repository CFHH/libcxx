# coding=utf-8
import os
import sys
import wast_builder

libc_dir = r"E:\Github\libc"
libcxx_dir = r"E:\Github\libcxx"
outname = 'app'

base_path = os.path.abspath(os.curdir)
# print(base_path)  # 这是命令行的当前目录
# for arg in sys.argv:
#     print(arg)


# cpp代码文件
source_files = []
cnt = len(sys.argv)
i = 0
while i < cnt - 1:
    i = i + 1
    arg = sys.argv[i]
    # print(arg)
    if arg[0] == '-':
        i = i + 1
        option = arg
        param = sys.argv[i]
        if option == '-o':
            outname = param
    else:
        source_files.append(os.path.join(base_path, arg))


# include文件夹
include_foders = []
include_foders.append(base_path)
include_foders.append(os.path.join(libcxx_dir, r"include"))
include_foders.append(os.path.join(libc_dir, r"include"))
# include_foders.append(os.path.join(boost_dir, r"include"))


# 输出文件夹
destination_foder = os.path.join(base_path, r"build")
if not os.path.exists(destination_foder):
    os.mkdir(destination_foder)


# 编译
linked_bc_file = os.path.join(destination_foder, 'linked.bc')
assembly_file = os.path.join(destination_foder, 'assembly.s')
wast_file = os.path.join(destination_foder, outname + '.wast')
wasm_file = os.path.join(destination_foder, outname + '.wasm')

compile_cmd_common = 'clang -emit-llvm -Oz --target=wasm32 -nostdinc -nostdlib -nostdlibinc -ffreestanding -nostdlib -fno-threadsafe-statics -fno-rtti -fno-exceptions'
for folder in include_foders:
    compile_cmd_common = compile_cmd_common + " -I " + folder

link_cmd = 'llvm-link -only-needed -o ' + linked_bc_file
link_cmd = link_cmd + ' ' + os.path.join(libc_dir, 'build_bc\libc.bc')
link_cmd = link_cmd + ' ' + os.path.join(libcxx_dir, 'build_bc\libc++.bc')

cnt = len(source_files)
for file in source_files:
    print('Compiling file [', i, '/', cnt, ']: ', file, ' ......')
    clang_cmd = compile_cmd_common
    st = os.path.splitext(file)
    t = os.path.split(st[0])
    name = t[1]
    ext = st[1]
    bcfile = os.path.join(destination_foder, name + '.ll')
    if ext == '.c':
        clang_cmd = clang_cmd + ' -D_XOPEN_SOURCE=700'
    else:
        clang_cmd = clang_cmd + ' --std=c++14'
    clang_cmd = clang_cmd + ' -c ' + file + ' -o ' + bcfile
    # print(clang_cmd)
    returncode = wast_builder.callcmd(clang_cmd)
    if returncode != 0:
        exit()
    link_cmd = link_cmd + ' ' + bcfile

print('Linking ......')
# print(link_cmd)
returncode = wast_builder.callcmd(link_cmd)
if returncode != 0:
    exit()

print('Assembling ......')
# -march=wasm32不能有
assemble_cmd = 'llc -thread-model=single --asm-verbose=false' + ' -o ' + assembly_file + ' ' + linked_bc_file
# print(assemble_cmd)
returncode = wast_builder.callcmd(assemble_cmd)
if returncode != 0:
    exit()

print('Creating WAST: ' + wast_file + ' ......')
wast_cmd = 's2wasm -o ' + wast_file + ' -s 16384 ' + assembly_file
# print(wast_cmd)
returncode = wast_builder.callcmd(wast_cmd)
if returncode != 0:
    exit()

print('Creating WASM: ' + wasm_file + ' ......')
wasm_cmd = 'wasm-as ' + wast_file + ' -o ' + wasm_file
# print(wasm_cmd)
returncode = wast_builder.callcmd(wasm_cmd)
if returncode != 0:
    exit()

print('COMPLETE！')
