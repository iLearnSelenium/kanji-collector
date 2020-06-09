import json
class Hint:
    def __init__(self, hanviet, kunList, onList):
        self.hanviet = hanviet
        self.kun = [kun for kun in kunList]
        self.on = [on for on in onList]
    @classmethod
    def fromJson(cls, data):
        return cls(data['hanviet'], data['kun'], data['on'])
    def __repr__(self):
        return f'Hint({self.hanviet!r},{self.kun!r},{self.on!r})'
    def __str__(self):
        return f'{{"hanviet": "{self.hanviet!s}","kun": {self.kun!s},"on": {self.on!s}}}'
class Kanji:
    def __init__(self, radical, hint):
        self.radical = radical
        self.hint = hint
    @classmethod
    def fromJson(cls, data):
        return cls(data['radical'], Hint.fromJson(data['hint']))
    def __repr__(self):
            return f'Kanji({self.radical!r},{self.hint!r})'
    def __str__(self):
            return f'{{"radical": "{self.radical!s}","hint": {self.hint!s}}}'

# kanji = Kanji.fromJson(json.loads('{"radical": "一", "hint": {"hanviet": "Nhất", "kun": ["ひと-", "ひと.つ"], "on": ["イチ", "イツ"]}}'))
# print(kanji)
# print(f'{kanji!r}')
# print(f'{kanji!s}')
# print(kanji.__dict__)
# print(kanji.hint.__dict__)
# jsonData = json.dumps(kanji, default=lambda o: o.__dict__, ensure_ascii=False, indent=2).encode('utf8')
# print(jsonData.decode()) 