import shelve


class Option():
    '''基本操作'''

    def __init__(self, user: str, setting):
        '''初始化'''
        # 文件名："mcb + 用户名"
        filename = 'mcb_' + user
        self.setting = setting
        # 打开文件
        self.mcbSelf = shelve.open(filename)
