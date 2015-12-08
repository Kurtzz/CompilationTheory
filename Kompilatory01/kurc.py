__author__ = 'Przemyslaw Kurc'

import os
import sys
import re
import codecs


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()
    autor = re.findall('<META NAME="AUTOR" CONTENT="[^\"]+(.*?)">', content, re.IGNORECASE)
    dzial = re.findall('<META NAME="DZIAL" CONTENT="(.+)">', content, re.IGNORECASE)
    kluczowe = re.findall('<META NAME="KLUCZOWE_\d" CONTENT="(.+)">', content)
    newContent = re.search('<P>(.*?)<META', content, re.DOTALL).group(1)
    zdania = re.findall('([A-Z].*?(?!\d+\.)(?=[a-z]{4,}[\n!?.]+))', newContent)
    skroty = re.findall(' [a-z]{1,3}\.', newContent)
    liczbyInt = re.findall('(?:-?)([1-2][0-9]{4}|'
                           '3[0-1][0-9]{3}|'
                           '32[0-6][0-9]{2}|'
                           '327[0-5][0-9]|'
                           '3276[0-7]|'
                           '[1-9][0-9]{0,3}|'
                           '-32768)(?!.*?\D\1\2\D)', newContent, re.VERBOSE)

    liczbyFlout = re.findall('-?(\d*)\.((?(1)\d*|\d+))([eE][+-]\d+)?(?!.*\1\.\2)', newContent, re.VERBOSE)

    daty = re.findall('((?:\d{4}(?P<delimiter1>[-/.]))'
                      '((?:(?:0[1-9]|[12][0-9]|3[01])(?P=delimiter1)(?:0[13578]|1[02]))|'
                      '(?:(?:0[1-9]|[12][0-9]|30)(?P=delimiter1)(?:0[469]|11))|'
                      '(?:(?:0[1-9]|[12][0-9])(?P=delimiter1)02)))|'
                      '((?:(?:0[1-9]|[12][0-9]|3[01])(?P<delimiter2>[-/.])(?:0[13578]|1[02]))(?:(?P=delimiter2)\d{4}))|'
                      '(?:(?:0[1-9]|[12][0-9]|30)(?P<delimiter3>[-/.])(?:0[469]|11))(?:(?P=delimiter3)\d{4})|'
                      '(?:(?:0[1-9]|[12][0-9])(?P<delimiter4>[-/.])02)(?:(?P=delimiter4)\d{4})',
                      newContent, re.VERBOSE)

    daty2 = re.findall('(?P<date>\d{4}(?P<delimiter1>[-/.]))?'
                       '((?:(?:0[1-9]|[12][0-9]|3[01])' # 31 dni
                       '(?(date)(?P=delimiter1)|(?P<delimiter2>[-/.]))(?:0[13578]|1[02]))|' # miesiace 31 dniowe
                       '(?:(?:0[1-9]|[12][0-9]|30)' # 30 dni
                       '(?(date)(?P=delimiter1)|(?P<delimiter3>[-/.]))(?:0[469]|11))|' # miesiace 30 dniowe
                       '(?:(?:0[1-9]|[12][0-9])' # 29 dni
                       '(?(date)(?P=delimiter1)|(?P<delimiter4>[-/.]))02))' # 29 dniowy luty
                       '(?(date)|(?(delimiter2)(?P=delimiter2)\d{4}|' # jezeli nie bylo daty na poczatku
                       '(?(delimiter3)(?P=delimiter3)\d{4}|'
                       '(?(delimiter4)(?P=delimiter4)\d{4}))))',
                       newContent, re.VERBOSE)

    emaile = re.findall('[a-z0-9\-.]+ @ [a-z]+ (?: \. [a-z]+)+', newContent, re.VERBOSE) #dopracowac

    fp.close()
    print("nazwa pliku: %s" % filepath)
    print("autor: %s" % autor[0])
    print("dzial: %s" % dzial[0])
    print("slowa kluczowe: %s" % map(str, kluczowe))
    print("liczba zdan: %s" % zdania.__len__())
    print("liczba skrotow: %s" % set(skroty).__len__())
    print("liczba liczb calkowitych z zakresu int: %s" % map(str, liczbyInt).__len__())
    print("liczba liczb zmiennoprzecinkowych: %s" % liczbyFlout.__len__())
    print("liczba dat: %s" % daty2.__len__())
    print("liczba adresow email: %s" % emaile.__len__())
    print("\n")

try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)


