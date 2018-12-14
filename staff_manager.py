__layout={}
import os
#添加新员工
def add_staff(staff_str):
    #转化输入字符串为字典
    new_staff = dict(zip(__layout[1:],staff_str.split(',')))

    #判断输入数据完整性
    if (len(new_staff) != len(__layout) - 1) or (not new_staff['age'].isdigit()) or (not new_staff["phone"].isdigit()):
        print("错误的add命令格式")
        return
    f = open("./staff.txt",mode = 'r+')
    f.readline()
    #读取每行对比手机号()
    for line in f:
        line = dict(zip(__layout ,line.strip().split(',')))
        if new_staff['phone'] == line['phone']:
            print("重复的手机号")
            break
    else:
        #根据最后一行的id，写入新的员工信息
        f.write('{},{}\n'.format(int(line['id']) + 1,staff_str))
        print("成功添加1条数据")
    f.close()

#查找员工
def find_staff(find_str):
    condition_lst=[]

    find_lst = ''.join(find_str)
    if 'find' not in find_str or 'from' not in find_str :
        print("command without find or from keyword")
        return
    filed_lst = find_str[find_lst.index['find'] + 1,find_lst.index('from')]
     
#删除员工
def delete_staff(__id):
    if not __id.isdigit():
        print("错误的ID")
        return
    f_old = open("./staff.txt",mode = 'r')
    f_new = open("./staff.new",mode = 'w')
    flags = 0
    f_new.write(f_old.readline())
    for line in f_old:
        if line.split(',')[0] !=__id:
            f_new.write(line)
        else:
            flags += 1
    else:
        print("delete {} information".format(flags))
    f_old.close()
    f_new.close()
    os.rename("./staff.new","./staff.txt")

#获取用户命令
def input_command():
    cmd = input(">>>:").strip()
    if cmd == "":
        print("empty command")
        return
    cmd_anasys = (cmd.split())
    if cmd_anasys[0] == 'add' and len(cmd_anasys) == 3:
        print("go into add_staff")
        add_staff(cmd_anasys[2])
    elif cmd_anasys[0] == 'find':
        find_staff(cmd)
    elif cmd_anasys[0] == 'del':
        print("cmd of del")
    elif cmd_anasys[0] == 'UPDATE':
        print("cmd of update")
    elif cmd_anasys[0] == 'q':
        exit()
    else:
        print("error command")
        

def system_init():
    global __layout
    f = open("./staff.txt",mode = 'r')
    #读取首行保存为格式
    __layout = f.readline().strip().split(',')
    f.close()

system_init()#初始化系统
#find_staff("find name from staff where age > 20")
delete_staff('1')
while True:
    input_command()
