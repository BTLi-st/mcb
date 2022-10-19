import shelve
import pyperclip
import sys
import os

# os.chdir('C:\\mcb')
mcbShelf = shelve.open('mcb')  # 打开 mcb 文件

try:
    # 判断参数个数
    if len(sys.argv) == 3:
        # 保存指定键值
        if sys.argv[1].lower() == 'save':
            mcbShelf[sys.argv[2]] = pyperclip.paste()
        # 删除指定键值
        elif (sys.argv[1].lower() == 'delete' or sys.argv[1].lower() == 'del'):
            # 键值存在
            if sys.argv[2] in list(mcbShelf.keys()):
                del mcbShelf[sys.argv[2]]
                print(f"[{sys.argv[2]}] 已被删除")
            # 键值不存在，抛出异常
            else:
                # print(f"[{sys.argv[2]}] hasn't been existed.")
                raise Exception(f"[{sys.argv[2]}] 并不存在")
        # 指令错误，抛出异常
        else:
            raise Exception("指令错误")
    elif len(sys.argv) == 2:
        # 显示帮助
        if sys.argv[1].lower() == 'help':
            print('创建可更新的多重剪贴板\n')
            print(
                'MCB [[help] | [list] | [clear] | [key] | [[save] key] | [[[del] | [delete]] key]]\n'
            )
            print('  key     存储的键名')
            print('          单独使用时会将该键名下的内容复制在剪贴板上')
            print('  help    查看帮助')
            print('  list    展示所有条目')
            print('  clear   清除所有存储的内容')
            print('  save    以指定键名保存剪贴板中的内容')
            print('  del     删除指定的内容')
            print('  delete  删除指定的内容')
        # 展示所有条目
        elif sys.argv[1].lower() == 'list':
            # pyperclip.copy(str(list(mcbShelf.keys())))
            # 存储不为空
            if list(mcbShelf.keys()):
                for key in list(mcbShelf.keys()):
                    print(f"{key}:")
                    print(f"[{mcbShelf[key][:30]}...]\n")
            # 储存为空
            else:
                print("目前没有储存任何数据")
        # 清空储存
        elif sys.argv[1].lower() == 'clear':
            mcbShelf.clear()
        # 将内容复制到剪贴板
        elif sys.argv[1] in mcbShelf:
            pyperclip.copy(mcbShelf[sys.argv[1]])
            print(
                f"已将 [{sys.argv[1]}] 中的内容 [{mcbShelf[sys.argv[1]][:30]}...] 复制到剪贴板中"
            )
        # 指令错误，抛出异常
        else:
            # print("Command error.")
            raise Exception("指令错误")
    # 指令错误，抛出异常
    else:
        raise Exception("指令错误")
# 处理异常
except Exception as err:
    print('发生异常：' + str(err))
    if str(err) == "指令错误":
        print("键入 MCB HELP 以查看正确指令")
# 关闭文件
mcbShelf.close()
