__layout={}




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
        f.write('{},{},{},{},{},{}\n'.format(int(line['id']) + 1,new_staff['name'],new_staff['age'],new_staff['phone'],new_staff['dept'],new_staff['enroll_date']))
        print("成功添加1条数据")
    f.close()


#获取用户命令
def input_command():
    cmd = input(">>>:").strip()
    cmd_anasys = (cmd.split())
    if cmd_anasys[0] == 'add' and len(cmd_anasys) == 3:
        print("go into add_staff")
        add_staff(cmd_anasys[2])
    elif cmd_anasys[0] == 'find':
        print("cmd of find")
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
while True:
    input_command()
