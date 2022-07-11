import argparse
import re
import datetime
import io


class Highlight:
    def __init__(self, title, author, text, created_at, position):
        self.title = title
        self.author = author
        self.text = text
        self.created_at = created_at
        self.position = position


def parse(textfile):
    with io.open(textfile, 'r', encoding='utf_8_sig') as f:
        lines = [' '.join(line.split()) for line in f.read().splitlines()]

    highlights = []
    highlight_lines = []

    it = iter(range(len(lines)))
    for i in it:
        if '==========' == lines[i]:
            title_and_author = lines[i + 1]
            r = re.match(r'(.*) \((.*)\)', title_and_author)
            if r:
                title = r.group(1).lstrip(u'\ufeff')
                author = r.group(2)
            else:
                title = ''
                author = ''

            position_and_created_at = lines[i + 2]
            r = re.match(r'- .*位置No\. (.*)のハイライト \|作成日: (.*)', position_and_created_at)
            if r:
                position = r.group(1)
                created_at = r.group(2)
            else:
                position = ''
                created_at = ''

            highlight_text = ''.join(highlight_lines)
            highlight_lines = []

            if highlight_text != '<このアイテムのクリップの上限に達しました>' and highlight_text != '' and title != '' and author != '' and position != '' and created_at != '':
                created_at_date = datetime.datetime.strptime(re.sub('.曜日', '', created_at), '%Y年%m月%d日 %H:%M:%S')
                highlights.append(Highlight(title, author, highlight_text, created_at_date, position.split('-')))
            next(it)
            next(it)
        else:
            highlight_lines.append(lines[i])

    return highlights


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('textfile', type=str)
    args = parser.parse_args()

    parse(args.textfile)
