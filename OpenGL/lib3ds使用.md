lib3ds简单使用
=============

lib3ds是一个读取3ds文件的开源库，读取3ds文件，数据以树的形式存储，相同数据以链表形式存储。

#数据结构
Lib3dsFile
Lib3dsVector
Lib3dsMesh
Lib3dsFace

#lib3ds_file_load(str)
加载3ds文件

#lib3ds_file_free(Lib3dsFile)
释放3ds文件数据

#lib3ds_mesh_calculate_normals(Lib3dsMesh, Lib3dsVector*)
计算网面的法线，一次计算3个。