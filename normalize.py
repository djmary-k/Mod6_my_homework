# Вимоги до функції normalize:
# - приймає на вхід рядок та повертає рядок;
# - здійснює транслітерацію кириличних символів на латиницю;
# - замінює всі символи, крім літер латинського алфавіту та цифр, на символ '_';
# - транслітерація може не відповідати стандарту, але бути читабельною;
# - великі літери залишаються великими, а маленькі — маленькими після транслітерації.

import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'[^a-zA-Z0-9.]', '_', t_name) 
    # t_name = re.sub(r'\W[^\.]', '_', t_name)
    return t_name



# print(normalize('vfAsфлПР№;%вт09ю123_asd.mp3'))