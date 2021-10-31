import re
import sys

from SingleLog.log import Logger
from uao import register_uao
from . import lib_util

register_uao()


class Target:
    MainMenu = [
        '離開，再見',
        '人, 我是',
        '[呼叫器]',
    ]

    MainMenu_Exiting = [
        '【主功能表】',
        '您確定要離開',
    ]

    QueryPost = [
        '請按任意鍵繼續',
        '───────┘',
    ]

    InBoard = [
        '看板資訊/設定',
        '文章選讀',
        '相關主題'
    ]

    InBoardWithCursor = [
        '【',
        '看板資訊/設定',
    ]

    # (h)說明 (←/q)離開
    # (y)回應(X%)推文(h)說明(←)離開
    # (y)回應(X/%)推文 (←)離開

    InPost = [
        '瀏覽',
        '頁',
        ')離開'
    ]

    PostEnd = [
        '瀏覽',
        '頁 (100%)',
        ')離開'
    ]

    InWaterBallList = [
        '瀏覽',
        '頁',
        '說明',
    ]

    WaterBallListEnd = [
        '瀏覽',
        '頁 (100%)',
        '說明'
    ]

    PostIP_New = [
        '※ 發信站: 批踢踢實業坊(ptt.cc), 來自:'
    ]

    PostIP_Old = [
        '◆ From:'
    ]

    Edit = [
        '※ 編輯'
    ]

    PostURL = [
        '※ 文章網址'
    ]

    Vote_Type1 = [
        '◆ 投票名稱',
        '◆ 投票中止於',
        '◆ 票選題目描述'
    ]

    Vote_Type2 = [
        '投票名稱',
        '◆ 預知投票紀事',
    ]

    AnyKey = '任意鍵'

    InTalk = [
        '【聊天說話】',
        '線上使用者列表',
        '查詢網友',
        '顯示上幾次熱訊'
    ]

    InUserList = [
        '休閒聊天',
        '聊天/寫信',
        '說明',
    ]

    InMailBox = [
        '【郵件選單】',
        '鴻雁往返'
    ]

    InMailMenu = [
        '【電子郵件】',
        '我的信箱',
        '把所有私人資料打包回去',
        '寄信給帳號站長',
    ]

    PostNoContent = [
        '◆ 此文章無內容',
        AnyKey
    ]

    InBoardList = [
        '【看板列表】',
        '選擇看板',
        '只列最愛',
        '已讀/未讀'
    ]

    use_too_many_resources = [
        '程式耗用過多計算資源'
    ]

    Animation = [
        '★ 這份文件是可播放的文字動畫，要開始播放嗎？'
    ]

    CursorToGoodbye = MainMenu.copy()


def show(config, screen_queue, function_name=None):
    if config.log_level != Logger.TRACE:
        return

    if isinstance(screen_queue, list):
        for Screen in screen_queue:
            print('-' * 50)
            try:
                print(
                    Screen.encode(
                        sys.stdin.encoding, "replace").decode(
                        sys.stdin.encoding))
            except Exception:
                print(Screen.encode('utf-8', "replace").decode('utf-8'))
    else:
        print('-' * 50)
        try:
            print(screen_queue.encode(
                sys.stdin.encoding, "replace").decode(
                sys.stdin.encoding))
        except Exception:
            print(screen_queue.encode('utf-8', "replace").decode('utf-8'))

        print('len:' + str(len(screen_queue)))
    if function_name is not None:
        print('錯誤在 ' + function_name + ' 函式發生')
    print('-' * 50)


displayed = False


def vt100(ori_screen: str, no_color: bool = True) -> str:
    result = ori_screen

    # temp = None
    # for c in result.encode('utf-8'):
    #     if not temp:
    #         temp = f'bytes([{c}'
    #     else:
    #         temp += f', {c}'
    # temp += '])'
    # print(temp)

    if no_color:
        result = re.sub('\x1B\[[\d+;]*m', '', result)

    result = re.sub(r'[\x1B]', '=PTT=', result)

    # global displayed
    # if not displayed:
    #     display = ('★' in result)
    #     if display:
    #         displayed = True
    # else:
    #     display = False
    #
    # if display:
    #     print('=1=' * 10)
    #     print(result)
    #     print('=2=' * 10)

    # result = '\n'.join(
    #     [x.rstrip() for x in result.split('\n')]
    # )

    # 編輯文章時可能會有莫名的清空問題，需再注意
    # if result.endswith('=PTT=[H'):
    #     print('!!!!!!!!=PTT=[H=PTT=[H=PTT=!!!!!!!!!!!!!!!')
    while '=PTT=[H' in result:
        if result.count('=PTT=[H') == 1 and result.endswith('=PTT=[H'):
            break
        result = result[result.find('=PTT=[H') + len('=PTT=[H'):]
    while '=PTT=[2J' in result:
        result = result[result.find('=PTT=[2J') + len('=PTT=[2J'):]

    pattern_result = re.compile('=PTT=\[(\d+);(\d+)H$').search(result)
    last_position = None
    if pattern_result is not None:
        # print(f'Before [{pattern_result.group(0)}]')
        last_position = pattern_result.group(0)

    # 進入 PTT 時，有時候會連分類看版一起傳過來然後再用主功能表畫面直接繪製畫面
    # 沒有[H 或者 [2J 導致後面的繪製行數錯誤

    if '=PTT=[1;3H主功能表' in result:
        result = result[result.find('=PTT=[1;3H主功能表') + len('=PTT=[1;3H主功能表'):]

    # if '=PTT=[1;' in result:
    #     if last_position is None:
    #         result = result[result.rfind('=PTT=[1;'):]
    #     elif not last_position.startswith('=PTT=[1;'):
    #         result = result[result.rfind('=PTT=[1;'):]

    # print('-'*50)
    # print(result)
    result_list = re.findall('=PTT=\[(\d+);(\d+)H', result)
    for (line_count, space_count) in result_list:
        line_count = int(line_count)
        space_count = int(space_count)
        current_line = result[
                       :result.find(
                           f'[{line_count};{space_count}H'
                       )].count('\n') + 1
        # if display:
        #     print(f'>{line_count}={space_count}<')
        #     print(f'>{current_line}<')
        if current_line > line_count:
            # if LastPosition is None:
            #     pass
            # elif LastPosition != f'=PTT=[{line_count};{space_count}H':
            #     print(f'current_line [{current_line}]')
            #     print(f'line_count [{line_count}]')
            #     print('Clear !!!')
            # print(f'!!!!!!!!=PTT=[{line_count};{space_count}H')

            result_lines = result.split('\n')
            target_line = result_lines[line_count - 1]
            if f'=PTT=[{line_count};{space_count}H=PTT=[K' in result:
                # 如果有 K 則把該行座標之後，全部抹除
                target_line = target_line[:space_count - 1]

                # OriginIndex = -1
                origin_line = None
                # for i, line in enumerate(result_lines):
                for line in result_lines:
                    if f'=PTT=[{line_count};{space_count}H=PTT=[K' in line:
                        # OriginIndex = i
                        origin_line = line
                        break

                if origin_line.count('=PTT=') > 2:
                    origin_line = origin_line[
                                  :lib_util.findnth(origin_line, '=PTT=', 3)
                                  ]

                # result_lines[OriginIndex] = result_lines[OriginIndex].replace(
                #     origin_line,
                #     ''
                # )

                origin_line = origin_line[
                              len(f'=PTT=[{line_count};{space_count}H=PTT=[K'):
                              ]

                # log.showValue(
                #     Logger.INFO,
                #     'origin_line',
                #     origin_line
                # )

                new_target_line = f'{target_line}{origin_line}'
                result_lines[line_count - 1] = new_target_line
            result = '\n'.join(result_lines)
        elif current_line == line_count:
            # print(f'!!!!!=PTT=[{line_count};{space_count}H')
            current_space = result[
                            :result.find(
                                f'=PTT=[{line_count};{space_count}H'
                            )]
            current_space = current_space[
                            current_space.rfind('\n') + 1:
                            ]
            # if display:
            #     print(f'>>{current_space}<<')
            #     print(f'ori length>>{len(current_space)}<<')
            #     newversion_length = len(current_space.encode('big5uao', 'ignore'))
            #     print(f'newversion_length >>{newversion_length}<<')

            # current_space = len(current_space.encode('big5', 'replace'))
            current_space = len(current_space)
            # if display:
            #     print(f'!!!!!{current_space}')
            if current_space > space_count:
                # if display:
                #     print('1')
                result = result.replace(
                    f'=PTT=[{line_count};{space_count}H',
                    (line_count - current_line) * '\n' + space_count * ' '
                )
            else:
                # if display:
                #     print('2')
                result = result.replace(
                    f'=PTT=[{line_count};{space_count}H',
                    (line_count - current_line) * '\n' + (space_count - current_space) * ' '
                )
        else:
            result = result.replace(
                f'=PTT=[{line_count};{space_count}H',
                (line_count - current_line) * '\n' + space_count * ' '
            )

        # while '=PTT=[K' in result:
        #     Target = result[result.find('=PTT=[K'):]

        #     print(f'Target[{Target}]')

        #     index1 = Target.find('\n')
        #     index2 = Target.find('=PTT=')
        #     if index2 == 0:
        #         index = index1
        #     else:
        #         index = min(index1, index2)

        #     break
        #     Target = Target[:index]
        #     print('===' * 20)
        #     print(result)
        #     print('-=-' * 20)
        #     print(Target)
        #     print('===' * 20)
        #     result = result.replace(Target, '')

        # print(Target)
        # print('===' * 20)

    if last_position is not None:
        result = result.replace(last_position, '')

    # if display:
    #     print('-Final-' * 10)
    #     print(result)
    #     print('-Final-' * 10)
    return result


class VT100Parser:
    def _h(self):
        self._cursor_x = 0
        self._cursor_y = 0

    def _2j(self):
        self.screen = [''] * 24
        self.screen_length = dict()

    def _move(self, x, y):
        self._cursor_x = x
        self._cursor_y = y

    def _newline(self):
        self._cursor_x = 0
        self._cursor_y += 1

    def _k(self):
        self.screen[self._cursor_y] = self.screen[self._cursor_y][:self._cursor_x]

    def __init__(self, data, encoding):
        # self._data = data
        # http://ascii-table.com/ansi-escape-sequences-vt-100.php

        self._cursor_x = 0
        self._cursor_y = 0
        self.screen = [''] * 24
        self.screen_length = dict()

        data = data.decode(encoding, errors='replace')
        # print(data)

        # remove color
        data = re.sub('\x1B\[[\d+;]*m', '', data)
        data = re.sub(r'[\x1B]', '=ESC=', data)
        data = re.sub(r'[\r]', '', data)
        # print(data)

        xy_pattern = re.compile('^=ESC=\[[\d]+;[\d]+H')

        count = 0
        while data:
            count += 1
            while True:
                if data.startswith('=ESC=[H'):
                    data = data[len('=ESC=[H'):]
                    self._h()
                    continue
                elif data.startswith('=ESC=[2J'):
                    data = data[len('=ESC=[2J'):]
                    self._2j()
                    continue
                elif data.startswith('=ESC=[K'):
                    data = data[len('=ESC=[K'):]
                    self._k()
                    continue
                break

            xy_result = xy_pattern.search(data)
            if xy_result:
                xy_part = xy_result.group(0)
                # print('!=', xy_part)

                new_y = int(xy_part[6:xy_part.find(';')]) - 1
                new_x = int(xy_part[xy_part.find(';') + 1: -1])
                # print(new_x, new_y)
                self._move(new_x, new_y)

                data = data[len(xy_part):]

            else:
                if data[:1] == '\n':
                    data = data[1:]
                    self._newline()
                    continue
                # print(f'-{data[:1]}-{len(data[:1].encode("big5-uao", "replace"))}')

                if self._cursor_y not in self.screen_length:
                    self.screen_length[self._cursor_y] = len(self.screen[self._cursor_y].encode('big5-uao', 'replace'))

                current_line_length = self.screen_length[self._cursor_y]
                replace_mode = False
                if current_line_length < self._cursor_x:
                    append_space = ' ' * (self._cursor_x - current_line_length)
                    self.screen[self._cursor_y] += append_space
                elif current_line_length > self._cursor_x:
                    replace_mode = True

                next_newline = data.find('\n')
                next_newline = 1920 if next_newline < 0 else next_newline
                next_esc = data.find('=ESC=')
                next_esc = 1920 if next_esc < 0 else next_esc
                if next_esc == 0:
                    break
                current_index = min(next_newline, next_esc)

                current_data = data[:current_index]
                current_data_length = len(current_data.encode('big5-uao', 'replace'))

                # print('=', current_data, '=', current_data_length)
                if replace_mode:
                    current_line = self.screen[self._cursor_y][:self._cursor_x]
                    current_line += current_data
                    current_line += self.screen[self._cursor_y][self._cursor_x + len(current_data):]

                    self.screen[self._cursor_y] = current_line
                else:
                    self.screen[self._cursor_y] += current_data
                    self._cursor_x += current_data_length
                    self.screen_length[self._cursor_y] = self._cursor_x

                data = data[current_index:]

                # print('\n'.join(self.screen))
        # print('\n'.join(self._screen))
        # print('=' * 20)
        # print(data)

        # print('Spend', count, 'cycle')
        self.screen = '\n'.join(self.screen)


if __name__ == '__main__':
    # 看板警察
    screen = bytes([226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 226, 150, 132, 32, 32, 27, 91, 109, 27, 91, 72, 27, 91, 50, 74, 27, 91, 49, 59, 51, 55, 59, 52, 52, 109, 227, 128, 144, 228, 184, 187, 229, 138, 159, 232, 131, 189, 232, 161, 168, 227, 128, 145, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 27, 91, 51, 51, 109, 230, 137, 185, 232, 184, 162, 232, 184, 162, 229, 175, 166, 230, 165, 173, 229, 157, 138, 27, 91, 48, 59, 49, 59, 51, 55, 59, 52, 52, 109, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 13, 10, 27, 91, 52, 55, 109, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 13, 10, 27, 91, 48, 59, 51, 51, 59, 52, 55, 109, 226, 150, 133, 226, 150, 134, 226, 150, 134, 27, 91, 49, 59, 51, 54, 59, 52, 51, 109, 226, 151, 165, 27, 91, 52, 55, 109, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 226, 150, 136, 13, 10, 27, 91, 48, 59, 51, 48, 59, 52, 51, 109, 32, 32, 32, 32, 32, 45, 226, 148, 128, 96, 32, 32, 32, 32, 32, 27, 91, 49, 59, 51, 54, 109, 239, 191, 163, 239, 191, 163, 239, 191, 163, 32, 32, 32, 32, 32, 32, 239, 191, 163, 239, 191, 163, 239, 191, 163, 32, 32, 32, 32, 239, 191, 163, 239, 191, 163, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 239, 191, 163, 239, 191, 163, 239, 191, 163, 27, 91, 51, 48, 109, 239, 191, 163, 239, 191, 163, 27, 91, 51, 54, 109, 239, 191, 163, 32, 32, 32, 32, 32, 32, 32, 32, 13, 10, 27, 91, 48, 59, 52, 51, 109, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 27, 91, 51, 49, 109, 226, 150, 130, 226, 150, 131, 27, 91, 49, 59, 51, 48, 109, 32, 32, 32, 32, 32, 239, 184, 177, 32, 32, 32, 32, 32, 32, 32, 239, 189, 156, 32, 32, 32, 32, 32, 32, 32, 32, 239, 185, 168, 32, 32, 32, 32, 32, 27, 91, 48, 59, 51, 48, 59, 52, 51, 109, 239, 189, 156, 32, 32, 32, 32, 32, 92, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 226, 136, 163, 32, 32, 13, 10, 32, 92, 95, 32, 32, 32, 226, 136, 149, 32, 27, 91, 51, 51, 59, 52, 49, 109, 226, 151, 164, 27, 91, 48, 59, 52, 49, 109, 226, 150, 130, 32, 27, 91, 51, 49, 59, 52, 51, 109, 226, 150, 138, 27, 91, 51, 52, 109, 227, 128, 130, 27, 91, 51, 48, 109, 32, 32, 32, 47, 32, 32, 226, 136, 149, 32, 32, 239, 185, 141, 32, 239, 185, 168, 32, 32, 27, 91, 49, 109, 76, 95, 32, 32, 32, 32, 32, 32, 32, 32, 32, 27, 91, 48, 59, 51, 48, 59, 52, 51, 109, 124, 32, 32, 32, 32, 32, 32, 32, 32, 124, 32, 32, 226, 138, 165, 32, 32, 32, 32, 32, 32, 32, 27, 91, 49, 109, 239, 189, 156, 32, 32, 32, 27, 91, 48, 59, 51, 48, 59, 52, 51, 109, 46, 226, 136, 160, 32, 32, 32, 13, 10, 32, 32, 32, 226, 149, 179, 32, 32, 32, 32, 27, 91, 51, 49, 59, 52, 55, 109, 226, 150, 138, 27, 91, 51, 48, 109, 203, 153, 27, 91, 48, 59, 52, 49, 109, 226, 150, 142, 27, 91, 51, 51, 109, 226, 151, 164, 27, 91, 51, 49, 59, 52, 51, 109, 226, 150, 142, 27, 91, 51, 48, 109, 96, 226, 148, 144, 32, 226, 148, 130, 44, 32, 32, 32, 239, 184, 179, 226, 150, 129, 32, 32, 32, 226, 149, 147, 45, 46, 239, 184, 191, 32, 32, 32, 226, 136, 149, 32, 32, 96, 32, 95, 239, 184, 179, 32, 226, 136, 163, 32, 46, 32, 32, 95, 120, 95, 32, 32, 32, 32, 92, 32, 32, 32, 239, 189, 156, 32, 226, 149, 178, 32, 13, 10, 32, 76, 32, 32, 27, 91, 51, 54, 109, 95, 226, 150, 132, 27, 91, 52, 49, 109, 226, 150, 138, 27, 91, 51, 48, 109, 92, 32, 27, 91, 51, 49, 59, 52, 55, 109, 226, 150, 134, 27, 91, 49, 59, 51, 54, 59, 52, 49, 109, 39, 32, 32, 32, 32, 27, 91, 48, 59, 51, 48, 59, 52, 51, 109, 32, 78, 32, 239, 188, 188, 95, 55, 95, 239, 184, 183, 45, 43, 226, 148, 164, 32, 226, 134, 150, 226, 149, 179, 32, 32, 32, 227, 128, 137, 226, 148, 172, 39, 226, 148, 140, 226, 128, 181, 226, 136, 154, 32, 55, 226, 149, 180, 46, 45, 239, 188, 129, 226, 128, 178, 32, 32, 32, 96, 226, 148, 172, 43, 226, 148, 188, 61, 46, 226, 136, 149, 61, 32, 226, 149, 180, 13, 10, 226, 148, 164, 32, 27, 91, 51, 51, 59, 52, 54, 109, 226, 150, 132, 32, 27, 91, 51, 49, 109, 226, 150, 132, 27, 91, 51, 48, 59, 52, 49, 109, 44, 32, 226, 149, 178, 44, 95, 32, 32, 27, 91, 51, 51, 109, 226, 151, 162, 27, 91, 51, 48, 59, 52, 51, 109, 226, 148, 130, 92, 95, 226, 149, 177, 226, 150, 143, 92, 95, 226, 136, 149, 95, 239, 185, 128, 32, 32, 95, 59, 125, 226, 128, 148, 76, 32, 32, 226, 134, 152, 95, 227, 128, 149, 45, 95, 226, 149, 179, 32, 32, 124, 32, 32, 32, 239, 188, 188, 95, 95, 70, 32, 226, 134, 153, 32, 32, 239, 185, 141, 93, 32, 226, 150, 143, 95, 226, 136, 149, 32, 13, 10, 32, 226, 149, 178, 27, 91, 51, 50, 109, 114, 27, 91, 52, 54, 109, 226, 150, 142, 27, 91, 51, 49, 109, 226, 151, 165, 27, 91, 51, 48, 59, 52, 49, 109, 227, 128, 131, 226, 148, 148, 27, 91, 51, 52, 109, 95, 27, 91, 51, 54, 109, 226, 150, 132, 27, 91, 51, 49, 59, 52, 51, 109, 227, 128, 158, 27, 91, 51, 48, 109, 226, 134, 151, 226, 149, 179, 32, 226, 150, 149, 95, 32, 226, 148, 152, 226, 149, 179, 32, 226, 149, 178, 95, 226, 134, 153, 226, 150, 142, 226, 134, 153, 226, 134, 145, 95, 226, 150, 149, 32, 32, 44, 226, 148, 188, 226, 150, 149, 32, 32, 239, 185, 168, 32, 32, 239, 185, 128, 96, 32, 32, 226, 150, 142, 96, 239, 191, 163, 32, 32, 226, 134, 150, 239, 191, 163, 125, 32, 226, 149, 178, 13, 10, 32, 114, 226, 148, 152, 32, 27, 91, 51, 51, 59, 52, 54, 109, 226, 150, 132, 32, 27, 91, 51, 49, 109, 226, 151, 165, 27, 91, 51, 51, 109, 226, 150, 131, 226, 150, 134, 27, 91, 51, 48, 59, 52, 51, 109, 226, 148, 172, 226, 149, 157, 226, 148, 148, 32, 226, 150, 142, 32, 32, 226, 149, 178, 32, 96, 32, 226, 150, 143, 226, 148, 156, 32, 32, 239, 191, 163, 92, 32, 32, 226, 128, 153, 239, 184, 186, 226, 150, 143, 27, 91, 51, 53, 109, 229, 143, 175, 228, 184, 141, 229, 143, 175, 228, 187, 165, 229, 129, 182, 231, 136, 190, 228, 184, 139, 233, 155, 168, 228, 184, 141, 229, 191, 133, 230, 176, 184, 233, 129, 160, 230, 153, 180, 229, 164, 169, 46, 46, 46, 27, 91, 49, 51, 59, 50, 51, 72, 27, 91, 109, 40, 27, 91, 49, 59, 51, 54, 109, 65, 27, 91, 109, 41, 110, 110, 111, 117, 110, 99, 101, 32, 32, 32, 32, 32, 227, 128, 144, 32, 231, 178, 190, 232, 143, 175, 229, 133, 172, 228, 189, 136, 230, 172, 132, 32, 227, 128, 145, 27, 91, 49, 52, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 70, 27, 91, 109, 41, 97, 118, 111, 114, 105, 116, 101, 32, 32, 32, 32, 32, 227, 128, 144, 32, 230, 136, 145, 32, 231, 154, 132, 32, 230, 156, 128, 230, 132, 155, 32, 227, 128, 145, 27, 91, 49, 53, 59, 50, 49, 72, 62, 32, 40, 27, 91, 49, 59, 51, 54, 109, 67, 27, 91, 109, 41, 108, 97, 115, 115, 27, 91, 49, 53, 59, 51, 56, 72, 227, 128, 144, 32, 229, 136, 134, 231, 181, 132, 232, 168, 142, 232, 171, 150, 229, 141, 128, 32, 227, 128, 145, 27, 91, 49, 54, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 77, 27, 91, 109, 41, 97, 105, 108, 27, 91, 49, 54, 59, 51, 56, 72, 227, 128, 144, 32, 231, 167, 129, 228, 186, 186, 228, 191, 161, 228, 187, 182, 229, 141, 128, 32, 227, 128, 145, 27, 91, 49, 55, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 84, 27, 91, 109, 41, 97, 108, 107, 27, 91, 49, 55, 59, 51, 56, 72, 227, 128, 144, 32, 228, 188, 145, 233, 150, 146, 232, 129, 138, 229, 164, 169, 229, 141, 128, 32, 227, 128, 145, 27, 91, 49, 56, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 85, 27, 91, 109, 41, 115, 101, 114, 27, 91, 49, 56, 59, 51, 56, 72, 227, 128, 144, 32, 229, 128, 139, 228, 186, 186, 232, 168, 173, 229, 174, 154, 229, 141, 128, 32, 227, 128, 145, 27, 91, 49, 57, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 88, 27, 91, 109, 41, 121, 122, 27, 91, 49, 57, 59, 51, 56, 72, 227, 128, 144, 32, 231, 179, 187, 231, 181, 177, 232, 179, 135, 232, 168, 138, 229, 141, 128, 32, 227, 128, 145, 27, 91, 50, 48, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 80, 27, 91, 109, 41, 108, 97, 121, 27, 91, 50, 48, 59, 51, 56, 72, 227, 128, 144, 32, 229, 168, 155, 230, 168, 130, 232, 136, 135, 228, 188, 145, 233, 150, 146, 32, 227, 128, 145, 27, 91, 50, 49, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 78, 27, 91, 109, 41, 97, 109, 101, 108, 105, 115, 116, 32, 32, 32, 32, 32, 227, 128, 144, 32, 231, 183, 168, 231, 137, 185, 229, 136, 165, 229, 144, 141, 229, 150, 174, 32, 227, 128, 145, 27, 91, 50, 50, 59, 50, 51, 72, 40, 27, 91, 49, 59, 51, 54, 109, 71, 27, 91, 109, 41, 111, 111, 100, 98, 121, 101, 27, 91, 50, 50, 59, 52, 49, 72, 233, 155, 162, 233, 150, 139, 239, 188, 140, 229, 134, 141, 232, 166, 139, 226, 128, 166, 13, 10, 10, 27, 91, 51, 52, 59, 52, 54, 109, 91, 49, 50, 47, 50, 32, 230, 152, 159, 230, 156, 159, 228, 184, 137, 32, 49, 55, 58, 52, 50, 93, 27, 91, 49, 59, 51, 51, 59, 52, 53, 109, 32, 91, 32, 229, 176, 132, 230, 137, 139, 230, 153, 130, 32, 93, 32, 32, 32, 27, 91, 51, 48, 59, 52, 55, 109, 32, 231, 183, 154, 228, 184, 138, 27, 91, 51, 49, 109, 54, 57, 51, 50, 48, 27, 91, 51, 48, 109, 228, 186, 186, 44, 32, 230, 136, 145, 230, 152, 175, 27, 91, 51, 49, 109, 106, 97, 110, 105, 99, 101, 48, 48, 49, 27, 91, 51, 48, 109, 32, 32, 32, 32, 32, 32, 91, 229, 145, 188, 229, 143, 171, 229, 153, 168, 93, 27, 91, 51, 49, 109, 233, 151, 156, 233, 150, 137, 32, 27, 91, 109, 27, 91, 49, 53, 59, 50, 49, 72])
    # screen = screen.decode('utf-8')
    # print(screen)

    p = VT100Parser(screen, 'utf-8')
    print(p.screen)
