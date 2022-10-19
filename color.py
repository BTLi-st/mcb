class Color:
    '''文字颜色'''

    def __init__(self):
        self.HEADER = '\033['
        self.ENDC = '\033[0m'
        self.DEFAULT = '0'
        self.HIGHLIHT = '1'
        self.NON_BOLD = '22'
        self.UNDERLINE = '4'
        self.NON_UNDERLINE = '24'
        self.FLASH = '5'
        self.NON_FLASH = '25'
        self.INVERSE = '7'
        self.NON_INVERSE = '27'
        self.FORECOLOR_BLACK = '30'
        self.FORECOLOR_RED = '31'
        self.FORECOLOR_GREEN = '32'
        self.FORECOLOR_YELLOW = '33'
        self.FORECOLOR_BLUE = '34'
        self.FORECOLOR_MAGENTA = '35'
        self.FORECOLOR_CYAN = '36'
        self.FORECOLOR_WHITE = '37'
        self.BACKCOLOR_BLACK = '40'
        self.BACKCOLOR_RED = '41'
        self.BACKCOLOR_GREEN = '42'
        self.BACKCOLOR_YELLOW = '43'
        self.BACKCOLOR_BLUE = '44'
        self.BACKCOLOR_MAGENTA = '45'
        self.BACKCOLOR_CYAN = '46'
        self.BACKCOLOR_WHITE = '47'

    def color(self, Type: str, Forecolor='', Backcolor=''):
        output = self.HEADER + Type
        if Forecolor != '':
            output = output + ';' + Forecolor
        if Backcolor != '':
            if Forecolor == '':
                output = output + ';' + self.FORECOLOR_WHITE + ';' + Backcolor
            else:
                output = output + ';' + Backcolor
        output = output + 'm'
        return output
