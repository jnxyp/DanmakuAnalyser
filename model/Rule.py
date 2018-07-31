import re

from model.Danmaku import Danmaku
from config.Constants import *


def _p(s: str, end='\n'):
    if DEBUG:
        print(s, end=end)


class Rule:
    subrules = []
    pattern = None

    def __init__(self, pattern, subrules):
        self.pattern = pattern
        self.subrules = subrules

    def __str__(self):
        return self.pattern.pattern

    def match(self, danmaku: Danmaku):
        return self.pattern.findall(danmaku.content)

    @staticmethod  # TODO Rewrite this parser
    def parse(rule_str: str, level: int = 0):

        pattern = re.compile(rule_str)

        if level % 2 == 0:
            subrule_strs = Rule._split_by_line(rule_str)
        else:
            subrule_strs = Rule._split_by_brackets(rule_str)

        subrules = []

        # Debug: print parsing tree
        _p('\n' + str(level) + '\t' + '|   ' * level + '├───┬' + rule_str, end='')

        for subrule_str in subrule_strs:
            subrules.append(Rule.parse(subrule_str, level + 1))

        if len(subrules) == 1 and subrule_strs[0] == rule_str and len(subrules[0].subrules) == 0:
            _p(' <- Cannot split!', end='')
            return Rule(pattern, [])
        return Rule(pattern, subrules)

    @staticmethod
    def _split_by_line(s: str):
        in_brackets = 0
        i = -1
        j = 0
        subrules = []
        while j < len(s):
            # Count bracket
            if s[j] == '(' and s[i - 1] != '\\':
                in_brackets += 1
            elif s[j] == ')' and s[i - 1] != '\\':
                in_brackets -= 1
            # Split string by '|' out of all the brackets
            if s[j] == '|' and s[i - 1] != '\\' and not in_brackets:
                subrules.append(s[i + 1:j])
                i = j
            j += 1
        subrules.append(s[i + 1:j])
        return subrules

    @staticmethod
    def _split_by_brackets(s: str):
        in_brackets = 0
        i = 0
        subrules = []
        text = ''
        while i < len(s):
            # Count bracket
            if s[i] == '(' and s[i - 1] != '\\':
                in_brackets += 1
            elif s[i] == ')' and s[i - 1] != '\\':
                in_brackets -= 1
            # Split string in bracket
            if in_brackets:
                text += s[i]
            elif len(text) > 0:
                subrules.append(text[1:])
                text = ''
            i += 1
        return subrules


if __name__ == '__main__':
    # sample = "((1|0(00)*01)((11|10(00)*01))*|(0(00)*1|(1|0(00)*01)((11|10(00)*01))*(0|10(00)*1))((1(00)*1|(0|1(00)*01)((11|10(00)*01))*(0|10(00)*1)))*(0|1(00)*01)((11|10(00)*01))*)"
    # rule = Rule.parse(sample)
    pattern = re.compile('ab')
    string = 'abcdaaaaaascdaderafgb'
    print(pattern.findall(string))
