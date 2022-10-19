class Settings:

    def __init__(self):
        self.workpath = 'C:\\mcb'
        self.keywordss = {
            'help': 0,
            'list': 0,
            'clear': 0,
            'save': 1,
            'del': 1,
            'delete': 1,
            'show': 1,
            'edit': 1,
            'key': 0,
            'ver': 0,
            'paste': -1,
            'keywords': 0,
            'rename': 1,
            'check': 0,
        }
        self.discription = {
            'help': ['查看帮助'],
            'list': ['展示所有标签及其内容预览'],
            'clear': ['清除所有存储的标签及其内容'],
            'save': ['以指定标签保存剪贴板中的内容'],
            'del': ['删除指定的标签及其内容'],
            'delete': ['删除指定的标签及其内容'],
            'show': ['完全展示指定标签的内容', '当指定标签名为 paste 时，将显示剪贴板中的内容'],
            'edit': ['编辑指定标签的内容'],
            'key': ['不同内容对应的标签', '单独使用时会将该标签下的内容复制在剪贴板上'],
            'ver': ['显示版本'],
            'paste': [],
            'keywords': ['显示所有关键字'],
            'rename': ['重命名标签'],
            'check': ['进行自检'],
        }
