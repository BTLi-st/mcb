# -*- coding=utf-8 -*-
import shelve
import pyperclip
import sys
import os
from color import Color


class Mcb():
    '''创建可更新的多重剪贴板'''

    def __init__(self):
        '''初始化'''
        # 创建或打开 mcb 文件
        # 调试时关闭
        # os.chdir('C:\\mcb')
        self.mcbSelf = shelve.open('mcb')
        self.keywords = [
            'help', 'list', 'clear', 'save', 'del', 'delete', 'show', 'edit',
            'key', 'ver', 'paste', 'keywords', 'rename', 'check'
        ]

    def CheckArgv(self):
        '''参数'''
        # 判断参数个数
        if len(sys.argv) == 4:
            # 重命名标签
            if self.cmp(sys.argv[1], 'rename'):
                self.RenameKey(sys.argv[2], sys.argv[3])
            else:
                raise Exception('指令错误')
        elif len(sys.argv) == 3:
            # 保存指定标签下的内容
            if self.cmp(sys.argv[1], 'save'):
                self.SaveNew(sys.argv[2], pyperclip.paste())
            # 删除指定标签下的内容
            elif self.cmp(sys.argv[1], 'del') or self.cmp(
                    sys.argv[1], 'delete'):
                self.DelPaste(sys.argv[2])
            # 展示特定标签下的内容
            elif self.cmp(sys.argv[1], 'show'):
                self.ShowOne(sys.argv[2])
            # 编辑特定标签下的内容
            elif self.cmp(sys.argv[1], 'edit'):
                self.EditOne(sys.argv[2])
            # 无法识别的指令
            else:
                raise Exception('指令错误')
        elif len(sys.argv) == 2:
            # 显示帮助
            if self.cmp(sys.argv[1], 'help'):
                self.ShowHelp()
            # 展示所有标签及其内容
            elif self.cmp(sys.argv[1], 'list'):
                self.ListAll()
            # 清空储所有标签及其内容
            elif self.cmp(sys.argv[1], 'clear'):
                self.ClearPaste()
            # 版本号
            elif self.cmp(sys.argv[1], 'ver') or self.cmp(
                    sys.argv[1], 'version'):
                self.Version()
            # 显示所有关键字
            elif self.cmp(sys.argv[1], 'keywords'):
                self.ShowKeywords()
            # 检测
            elif self.cmp(sys.argv[1], 'check'):
                self.Check()
            # 将指定标签下的内容复制到剪贴板
            elif self.check_paste_exist(sys.argv[1]):
                self.PutPaste(sys.argv[1])
            # 无法识别的指令
            else:
                raise Exception(
                    f'指令错误或标签 {self.colorful_key(sys.argv[1])} 并不存在')
        # 无法识别的指令
        else:
            raise Exception('没有任何参数输入\n输入 mcb help 以查看语法规则')

    def RenameKey(self, key, new_name, answer=False, show=True):
        '''重命名标签'''
        if self.check_paste_exist(key):
            if self.cmp(key, new_name):
                return
            if not self.SaveNew(new_name, self.mcbSelf[key][:], answer, show):
                return False
            self.mcbSelf.pop(key)
            if show:
                print(
                    f'已将 {self.colorful_key(key)} 重命名为 {self.colorful_key(new_name)}'
                )
            return True
        else:
            self.NOT_EXITED_ERROR(key)

    def SaveNew(self, key, value, answer=False, show=True):
        '''在指定标签下保存新内容'''
        if self.check_paste_exist(key):
            if answer or self.get_answer(
                    self.colorful_warning('当前标签 ') + self.colorful_key(key) +
                    self.colorful_warning(' 下已有内容，是否覆盖？（Y / n）')):
                self.SavePaste(key, value)
                if show:
                    print(f'已更新 {self.colorful_key(key)} 中的内容')
            else:
                return False
        else:
            self.SavePaste(key, value)
            if show:
                print('保存成功：')
                self.ShowPaste(key)
        return True

    def SavePaste(self, key, value):
        '''保存标签下的内容'''
        self.check_keywords(key)
        self.mcbSelf[key] = value

    def DelPaste(self, key, answer=False):
        '''删除标签及其内容'''
        # 标签存在
        if self.check_paste_exist(key):
            if answer or self.get_answer(
                    self.colorful_warning('确认删除标签 ') + self.colorful_key(key) +
                    self.colorful_warning(' 及其内容吗？（Y / n）')):
                del self.mcbSelf[key]
        # 标签不存在，抛出异常
        else:
            self.NOT_EXITED_ERROR(key)

    def ClearPaste(self, answer=False):
        '''清理所有标签及其内容'''
        # 有标签
        if list(self.mcbSelf.keys()):
            if answer or self.get_answer(
                    self.colorful_warning('当前操作将清除所有标签及其内容，是否继续？（Y / n）')):
                self.mcbSelf.clear()
        # 无标签
        else:
            print(self.colorful_warning('目前没有储存任何内容'))

    def Version(self):
        '''显示版本号'''
        print('MCB [版本 1.5]')

    def ShowHelp(self):
        '''显示提示'''
        print('创建可更新的多重剪贴板\n')
        print(
            'MCB [[help] | [list] | [clear] | [key] | [ver] | [check] | [keywords] | [[save] key] | [[[del] | [delete]] key] | [[show] key] | [[edit] key]] | [[rename] key new_name]\n'
        )
        self.output_format('key', '不同内容对应的标签')
        self.output_format('', '单独使用时会将该标签下的内容复制在剪贴板上')
        self.output_format('help', '查看帮助')
        self.output_format('list', '展示所有标签及其内容预览')
        self.output_format('clear', '清除所有存储的标签及其内容')
        self.output_format('save', '以指定标签保存剪贴板中的内容')
        self.output_format('del', '删除指定的标签及其内容')
        self.output_format('delete', '删除指定的标签及其内容')
        self.output_format('show', '完全展示指定标签的内容')
        self.output_format('', '当指定标签名为 paste 时，将显示剪贴板中的内容')
        self.output_format('edit', '编辑指定标签的内容')
        self.output_format('rename', '重命名标签')
        self.output_format('ver', '显示版本')
        self.output_format('version', '显示版本')
        self.output_format('keywords', '显示所有关键字')
        self.output_format('check', '进行自检')
        print(self.colorful_warning('\n注意：以上这些关键字均不能用作标签名'))

    def ListAll(self):
        '''展示所有标签及其内容'''
        # 有标签
        if list(self.mcbSelf.keys()):
            for key in list(self.mcbSelf.keys()):
                self.ShowPaste(key)
        # 没有任何标签
        else:
            print(self.colorful_warning('目前没有储存任何内容'))

    def ShowKeywords(self):
        '''显示所有的关键字'''
        print('以下为所有关键字：')
        for keyword in self.keywords:
            print(self.colorful_key(keyword))
        print(self.colorful_warning('注意：这些关键字均不能作为标签名使用'))

    def ShowOne(self, key):
        '''展示特定标签及其内容'''
        if self.check_paste_exist(key) or self.cmp(key, 'paste'):
            self.ShowPaste(key, 0)
        else:
            self.NOT_EXITED_ERROR(key)

    def EditOne(self, key, answer=False, show=True):
        '''编辑特定标签及其内容'''
        # 新建文件并写入剪贴板上的内容
        # 没有此标签
        if (not self.check_paste_exist(key)):
            if answer or self.get_answer(
                    self.colorful_warning('不存在此标签，是否创建一个空标签？（Y / n）')):
                self.SavePaste(key, '')
            else:
                return
        filename = f'{key}.txt'
        edit_file = open(filename, 'w', encoding='utf-8')
        edit_file.write(self.mcbSelf[key])
        edit_file.close()
        # 打开文件
        os.system(filename)
        # 读取文件更新内容
        edit_file = open(filename, 'r', encoding='utf-8')
        self.SavePaste(key, edit_file.read())
        edit_file.close()
        # 删除文件
        os.remove(filename)
        # 提示
        if show:
            print(f'成功更新 {self.colorful_key(key)} 中的内容')

    def ShowPaste(self, key, num=30):
        '''展示内容'''
        print(f'{self.colorful_key(key)}')
        if key == 'paste':
            print(pyperclip.paste())
        else:
            if num == 0 or len(self.mcbSelf[key]) <= num:
                print(f'{self.mcbSelf[key][:]}\n')
            else:
                print(f'{self.mcbSelf[key][:num]}...\n')

    def PutPaste(self, key, show=True):
        '''将内容放在剪贴板上'''
        pyperclip.copy(self.mcbSelf[key])
        if show:
            print('已将内容：')
            self.ShowPaste(key)
            print('放到剪贴板上')

    def Check(self, show=True):
        '''自检'''
        if show:
            print('开始进行自检')
        try:
            # 检测关键字
            if show:
                print('关键字检测')
            for key in self.mcbSelf.keys():
                if self.check_keywords(key, False):
                    # 是关键字
                    self.solve_problem_keywords(key)
            if show:
                print(
                    f'{col.color(col.DEFAULT, col.FORECOLOR_GREEN)}关键字检测完成{col.ENDC}'
                )
            # 去除空白
            if show:
                print('开始查找空白标签')
            keys = []
            # 查找空白
            for key in self.mcbSelf.keys():
                if self.cmp(self.mcbSelf[key], ''):
                    keys.append(key)
            #  处理空白
            if keys:
                self.sholve_problem_None(keys)
            if show:
                print(f'{col.color(col.DEFAULT, col.FORECOLOR_GREEN)}检测完成{col.ENDC}')
            # 查重
            if show:
                print('开始查重')
            values = {}
            # 反映射
            for key in self.mcbSelf.keys():
                if self.mcbSelf[key] in values.keys():
                    values[self.mcbSelf[key]].append(key)
                else:
                    values[self.mcbSelf[key]] = [key]
            # 判断是否重复
            for value in values.keys():
                if len(values[value]) > 1:
                    self.solve_problem_repeating(values[value])
            if show:
                print(
                    f'{col.color(col.DEFAULT ,col.FORECOLOR_GREEN)}查重处理完成{col.ENDC}'
                )
        except Exception as err:
            print(f'{col.color(col.DEFAULT,col.FORECOLOR_RED)}异常：{col.ENDC}' +
                  str(err))
            if self.get_answer(self.colorful_warning('是否重新进行自检？')):
                self.Check()

    def solve_problem_keywords(self, key, answer=False):
        '''关键字处理'''
        print(
            self.colorful_warning('储存的键值') + self.colorful_key(key) +
            self.colorful_warning('为关键字'))
        if answer or self.get_answer(
                self.colorful_warning('是否重命名？若否则会删除该标签（Y / n）')):
            while True:
                # 重命名
                new_name = input('请输入新标签名：')
                if self.RenameKey(key, new_name):
                    break
        else:
            # 删除
            self.DelPaste(key, True)

    def sholve_problem_None(self, keys: list):
        '''处理空标签'''
        print('以下标签内容均为空')
        for key in keys:
            print(self.colorful_key(key))
        if self.get_answer(self.colorful_warning('是否需要全部删除？（Y / n）')):
            for key in keys:
                # 删除空标签
                self.DelPaste(key, True)

    def solve_problem_repeating(self, keys: list):
        '''处理重复'''
        print('内容')
        self.ShowPaste(keys[0])
        print('以下标签内容与其重复')
        for key in keys[1:]:
            print(self.colorful_key(key))
        if self.get_answer(self.colorful_warning('是否需要合并？（Y / n）')):
            while True:
                # 存在该标签名，范围内修改
                new_name = input('请输入新标签名：')
                if new_name in keys:
                    for key in keys:
                        self.RenameKey(key, new_name, True, False)
                    break
                # 范围外修改
                else:
                    if self.RenameKey(keys[0], new_name, show=False):
                        for key in keys[1:]:
                            self.DelPaste(key, True)
                        break
        print('处理成功')

    def check_keywords(self, key, report=True):
        '''检测关键字'''
        if key in self.keywords:
            if report:
                raise Exception(f'关键字冲突，{self.colorful_key(key)} 不能用作标签名')
            else:
                return True
        return False

    def check_paste_exist(self, key):
        '''检查标签是否存在'''
        return key in self.mcbSelf

    def cmp(self, a: str, b: str):
        '''判断是否相同'''
        return a.lower() == b.lower()

    def output_format(self, name: str, intro: str):
        '''规范化输出'''
        formatted_name = '  ' + name + (' ' * (8 - len(name)))
        print(formatted_name + intro)

    def NOT_EXITED_ERROR(self, key):
        '''标签不存在错误'''
        raise Exception(f'{self.colorful_key(key)} 并不存在')

    def colorful_key(self, key):
        '''让标签具有颜色'''
        return col.color(col.HIGHLIHT,
                         col.FORECOLOR_BLUE) + '[' + key + ']' + col.ENDC

    def colorful_warning(self, warning):
        '''让警告具有颜色'''
        return col.color(col.DEFAULT,
                         col.FORECOLOR_YELLOW) + warning + col.ENDC

    def get_answer(self, question: str):
        '''询问问题'''
        while True:
            answer = input(question)
            if self.cmp(answer, 'y') or self.cmp(answer, 'yes'):
                return True
            elif self.cmp(answer, 'n') or self.cmp(answer, 'n'):
                return False


if __name__ == '__main__':
    # 运行程序
    mcb = Mcb()
    col = Color()
    try:
        mcb.CheckArgv()
    except Exception as err:
        print(f'{col.color(col.DEFAULT, col.FORECOLOR_RED)}异常：{col.ENDC}' +
              str(err))
