import re
import fileUtils
from selenium import webdriver


class KanjiBuilder:
    def __init__(self, radical):
        self.radical = str(radical)
        self.hanviet = []
        self.kun = []
        self.on = []
        self.strokes = None
        self.jlpt = None
        self.grade = None

    def addHanviet(self, hanviet):
        self.hanviet.append(str(hanviet))
        return self

    def addKun(self, kun):
        self.kun.append(str(kun))
        return self

    def addOn(self, on):
        self.on.append(str(on))
        return self

    def setMetadata(self, strokes, jlpt, grade):
        self.strokes = int(strokes)
        self.jlpt = str(jlpt) if jlpt is not None else None
        self.grade = int(grade)
        return self

    def build(self):
        return {
            'radical': self.radical,
            'hint': {
                'hanviet': [hanviet for hanviet in self.hanviet],
                'kun': [kun for kun in self.kun],
                'on': [on for on in self.on],
            },
            'metadata': {
                'strokes': self.strokes,
                'JLPT': self.jlpt,
                'grade': self.grade
            }
        }

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.maximize_window()
driver.implicitly_wait(10)  # 10 is in seconds
def collectKanjis(kanjis, url, page, pages):
    if pages is not None and page > pages:
        return
    driver.get(f'{url}?page={page}')
    print(f'{url}?page={page}')
    secondary = driver.find_element_by_id("secondary")
    resultCountStr = secondary.find_element_by_xpath(
        '//*[@id="secondary"]/div/h4/span').text

    regex = r"^— (\d+) found$"
    match = re.fullmatch(regex, resultCountStr)
    print(match.group(1))
    resultCount = int(match.group(1))
    limit = 20
    pages = int(resultCount//20 + (1 if resultCount % limit > 0 else 0))

    entries = secondary.find_elements_by_xpath(
        '//*[@id="secondary"]/div/div[@class="entry kanji_light clearfix"]')
    for entry in entries:
        builder = KanjiBuilder(entry.find_element_by_xpath(
            './/div[@class="kanji_light_content"]/div[@class="literal_block"]/span[@class="character literal japanese_gothic"]/a').text)
        infoStr = entry.find_element_by_xpath('.//div[@class="kanji_light_content"]/div[@class="info clearfix"]').text
        print(infoStr)
        infoRegex = r"^(\d+) stroke[s]*. [JLPT ]*(N\d)*[. ]*Jōyō kanji, taught in grade (\d).$"
        infoMatch = re.fullmatch(infoRegex, infoStr)
        builder.setMetadata(infoMatch.group(1), infoMatch.group(2), infoMatch.group(3))
        kunEntries = entry.find_elements_by_xpath('.//div[@class="kanji_light_content"]/div[@class="kun readings"]/span[@class="japanese_gothic "]/a')
        [print(k.text) for k in kunEntries]
        [builder.addKun(kunEntry.text) for kunEntry in kunEntries]
        onEntries = entry.find_elements_by_xpath('.//div[@class="kanji_light_content"]/div[@class="on readings"]/span[@class="japanese_gothic "]/a')
        [builder.addOn(onEntry.text) for onEntry in onEntries]
        kanjis.append(builder.build())
    collectKanjis(kanjis, url, page + 1, pages)
def main():
    jishoURLs = ['https://jisho.org/search/%20%23kanji%20%23grade:1',
                 'https://jisho.org/search/%20%23kanji%20%23grade:2',
                 'https://jisho.org/search/%20%23kanji%20%23grade:3',
                 'https://jisho.org/search/%20%23kanji%20%23grade:4',
                 'https://jisho.org/search/%20%23kanji%20%23grade:5',
                 'https://jisho.org/search/%20%23kanji%20%23grade:6',
                 ]
    kanjis = []
    for url in jishoURLs:
        collectKanjis(kanjis, url, 1, None)
    # kanji = KanjiBuilder('日').addHanviet('Nhật').addKun('ひ').addKun(
    #     '-び').addKun('-か').addOn('ニチ').addOn('ジツ').build()
    data = {}
    data['kanjis'] = kanjis
    fileUtils.writeKanjiDataToJson(data)


if __name__ == "__main__":
    main()