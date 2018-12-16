__layout = {}

def where_parser(condition):
    """
    parse condition and return the list of all items which match condition
    """
    flags=True
    match_list=[]
    match_item=[]
    condition = condition.split("where")
    if len(condition) == 2:
        condition = ''.join(condition[1])
    else:
        print("\033[0;31mEmpty format of [condition]\033[0;0m")
        return

    if '>' in condition and condition.count(">") == 1:
        filed,co_value = condition.split('>')
        if filed.strip() in __layout["format"]:
            for v,item in enumerate(__layout[filed.strip()]):
                if co_value.strip().isdigit() and int(item) > int(co_value):
                    match_item = [__layout[x][v] for x in __layout["format"]]
                    match_list.append(match_item)
        else:
            flags = False
    elif '<' in condition and condition.count('<') == 1:
        filed,co_value = condition.split('<')
        if filed.strip() in __layout["format"]:
            for v,item in enumerate(__layout[filed.strip()]):
                if co_value.strip().isdigit() and int(item) < int(co_value):
                    match_item = [__layout[x][v] for x in __layout["format"]]
                    match_list.append(match_item)
        else:
            flags = False
    elif '=' in condition and condition.count('=') == 1:
        filed,co_value = condition.split('=')
        if filed.strip() in __layout["format"]:
            for v,item in enumerate(__layout[filed.strip()]):
                if item == co_value.strip():
                    match_item = [__layout[x][v] for x in __layout["format"]]
                    match_list.append(match_item)
        else:
            flags = False
    elif 'like' in condition and condition.count("like") == 1:
        filed,co_value = condition.split('like')
        if filed.strip() in __layout["format"]:
            for v,item in enumerate(__layout[filed.strip()]):
                if co_value.strip() in item:
                    match_item = [__layout[x][v] for x in __layout["format"]]
                    match_list.append(match_item)
        else:
            flags = False
    else:
        print("Unknown operater in [condition]")
        return

    if flags == True:
        return match_list
    else:
        print("Unknown filed in [condition]")


def find_parser(func):
    def find_func(cmd_str):
        filed = cmd_str.strip("find").split('from')[0].split(',')
        filed = [x.strip() for x in filed]
        filed = list(filter(lambda x:x.strip() != '',filed))
        if '*' in filed:
            filed=__layout["format"]
        else:
            for i in filed:
                if i.strip() not in __layout["format"]:
                    print("filed {} unknown in [filed]".format(i))
                    return

        match_list = where_parser(cmd_str)#get match list
        if match_list == None:
            return
        func(match_list,filed)
    return find_func
@find_parser
def find_process(match_list,show_list):
    for item in match_list:
        [print(item[__layout["format"].index(x)],end='\t') for x in show_list]
        print()

def add_parser(func):
    def add_func(cmd_str):
        pass
    return add_func
@add_parser
def add_process():
    pass


def update_parser(func):
    def update_func(cmd_str):
        if 'update' and 'set' and 'where' in cmd_str:
            match_list = where_parser(cmd_str)
            if match_list != None:
                changed = cmd_str.split('set')[1].split('where')[0].split('=')
                changed = [x.strip() for x in changed]
                if len(changed) != 2 or '' in changed:
                    print("\033[0;31mUnknown motify in [changed]\033[0;0m")
                    return
                if changed[0] not in __layout["format"]:
                    print("filed {} unknown in [changed]".format(i))
                    return

                func(changed[0],changed[1],match_list)
        else:
            print("\033[0;31mToo few keywords of update\033[0;0m")

    return update_func
@update_parser
def update_process(motify_filed,motify_val,match_list):
    for item in match_list:
        s_id = int(item[__layout["format"].index('id')])
        __layout[motify_filed][s_id] = motify_val
    f = open("./staff.txt",mode = 'w')
    [f.write(','.join(x)) for x in __layout["format"]]
    line=[]
    for v,filed in __layout["format"]:
        line.append(__layout[filed][v])
        print(','.join(line))
    f.close()
    

def del_parser(func):
    def del_func(cmd_str):
        where_parser(''.join(cmd_str.split("where")[1]))
    return del_func
@del_parser
def del_process(cmd_str):
    pass

def syntax_parser(cmd_str):
    """
    paramenter cmd_str: command which has been strip() and not an "" or "q"
                        such as "find name,age from staff where age > 20"
    parse syntax and judge it is find or update or del or add
    """
    cmd_lst = cmd_str.split()
    #judge which command
    if cmd_lst[0] == "find":#find [filed1,[filed2]] from [table] where [condition]
        find_process(cmd_str)
    elif cmd_lst[0] == "add":#add [table] [name,age,phone,debt,enroll_date]
        add_process(cmd_str)
    elif cmd_lst[0] == "update":#update [table] set [changed] where [condition]
        update_process(cmd_str)
    elif cmd_lst[0] == "del":#del [table] where [condition]
        del_process(cmd_str)
    else:
        print("\033[0;31mERROR Command input\033[0m")

def load_data():
    """
    load file of staff information to memory
    store format is dict
    return : dict
    """
    global storage_format 
    layout = {}
    f = open("./staff.txt",mode = 'r')
    
    "read first line ,the first line discribe the format of storage"
    storage_format = f.readline().strip().split(',')
    layout["format"]=storage_format
    for item in storage_format:
        layout[item] = []
       
    for line in f:
        line = line.strip().split(',')
        for v,item in enumerate(line):
            layout[storage_format[v]].append(item)
    f.close()

    return layout

def main():
    """
    main function
    """
    global __layout
    __layout = load_data()#read
    while True:
        cmd = input(">>>").strip()
        if cmd == "q":
            exit("see you")
        if cmd != "":
            syntax_parser(cmd)

main()
