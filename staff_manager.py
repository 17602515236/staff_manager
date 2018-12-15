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


def find_checkout(func):
    def tmp_func(cmd):
        #解析find指令find [filed] from [table] where [condition]
        if 'find' in cmd and ' from ' in cmd and ' where ' in cmd:
            cmd = cmd.split()
            _filed = cmd[cmd.index('find') + 1:cmd.index('from')]
            _table = cmd[cmd.index('from') + 1:cmd.index('where')]
            _condition = cmd[cmd.index('where') + 1:]
            if len(_filed) == 0 or len(_table) == 0 or len(_condition) == 0:
                print("ERROR value of [filed] or [table] or [condition]")
                return
            print(_condition)
            print(_filed)
            if True not in [x in _condition for x in __layout] or True not in [x in _filed for x in __layout]:
                print("Unknown filed in [conditon] or in [filed]")
                return
            if 'like' in _condition:
                _condition_para = "{} in {}".format(_condition[2],_condition[0])
            elif :
                _condition_para = ''.join(_condition).replace('=','==')
            else:
                _condition_para = ''.join(_condition)
                print(_condition_para)

            if '*' in _filed:
                filed_para = list(range(len(__layout)))
            else:
                filed_para = [__layout.index(x) for x in _filed]
            
            func(filed_para,_condition_para)
        else:
            print("ERROR Format of command find")
            return
        ##############
    return tmp_func
#查找员工
@find_checkout
def find_staff(filed,condition_str):
    flags=0
    f = open("./staff.txt",mode = 'r')
    f.readline()
    for line in f:
        s_id = int(line.split(',')[0])
        name = line.split(',')[1]
        age = int(line.split(',')[2])
        phone = line.split(',')[3]
        dept = line.split(',')[4]
        enroll_date = line.split(',')[5]
        if eval(condition_str):
            print(','.join([line.split(',')[x] for x in filed]))
            flags += 1
    else:
        print("Find {} Staff informations".format(flags))
    f.close()
     




#删除员工
def delete_staff(cmd):
    cmd = cmd.split()
    if len(cmd) != 3:
        print("error number of arguments of del")
        return
    if not cmd[2].isdigit():
        print("input error")
        return
        
    f_old = open("./staff.txt",mode = 'r')
    f_new = open("./staff.new",mode = 'w')
    flags = 0
    f_new.write(f_old.readline())
    for line in f_old:
        if line.split(',')[0] != cmd[2]:
            f_new.write(line)
        else:
            flags += 1
    else:
        print("delete {} information".format(flags))
    f_old.close()
    f_new.close()
    os.rename("./staff.new","./staff.txt")



#修改用户信息
def motify_checkout(func):
    def tmp_func(cmd):
        if "UPDATE" in cmd and "SET" in cmd and 'WHERE' in cmd:
            cmd = cmd.split()
            _table = cmd[cmd.index('UPDATE') + 1:cmd.index('SET')]
            _motify = cmd[cmd.index('SET') + 1:cmd.index('WHERE')]
            _condition = cmd[cmd.index('WHERE') + 1:]

            _value= ''.join(_motify).split('=')[1]
            _motify = ''.join(_motify).split('=')[0]
            _condition = ''.join(_condition).replace("=","==")
            func(_motify,_value,_condition)
        else:
            print("ERROR Arguments in command UPDATE")
    return tmp_func

@motify_checkout
def motify_staff(motify,val,match):
    f = open("./staff.txt",mode = 'r')
    f1 = open("./staff.new",mode = 'w')
    f1.write(f.readline())
    for line in f:
        s_id = int(line.split(',')[0])
        name = line.split(',')[1]
        age = int(line.split(',')[2])
        phone = line.split(',')[3]
        dept = line.split(',')[4]
        enroll_date = line.split(',')[5]
        if eval(match):
            line = line.strip().split(',')
            line[__layout.index(motify)] = val
            f1.write(','.join(line) + '\n')
        else:
            f1.write(line)
    f.close()
    f1.close()
    os.rename("./staff.new","./staff.txt")


#获取用户命令
def input_command():
    cmd = input(">>>:").strip()
    if cmd == "":
        print("empty command")
        return
    cmd_anasys = (cmd.split())
    if cmd_anasys[0] == 'add' and len(cmd_anasys) == 3:
        add_staff(cmd_anasys[2])
    elif cmd_anasys[0] == 'find':
        find_staff(cmd)
    elif cmd_anasys[0] == 'del':
        delete_staff(cmd)
    elif cmd_anasys[0] == 'UPDATE':
        motify_staff(cmd)
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
#find_staff([__layout.index("name"),__layout.index("phone")],"age > 20")
#find_staff("find name * from staff where name like 'z'")
motify_staff("UPDATE A SET name='wwww' WHERE name='zhj'")
while True:
    input_command()
