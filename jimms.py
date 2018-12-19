from lxml import html
import requests
import re
import bs4
def itsefunktio():

    alennukset = "JIMMSIN TARJOUKSET\n"
    page = requests.get('https://www.jimms.fi')
    tree = html.fromstring(page.content)



    navigaatiomenu = tree.xpath('//div[@class="groupitems"]/a/@href')
    for i in navigaatiomenu:
        page1 = requests.get('https://www.jimms.fi{}'.format(i))
        tree1 = html.fromstring(page1.content)
        itemmenu = tree1.xpath('//div[@class="list-group-item menu"]/ul/li/a/@href')
        for c in itemmenu:

            page2 = requests.get('https://www.jimms.fi{}'.format(c))
            tree2 = html.fromstring(page2.content)
            items = tree2.xpath('//div[@class="p_col_info"]/div/a/text()')
            joo2 = tree2.xpath('//div[@class="p_col_price"]/div/text()')
            dap = []

            for i in joo2:
                if(len(i)>46):
                    dap.append(re.sub(' +',' ',i).strip('\r\n '))
                else:
                    pass
            for j in range(len(items)):
                kap = items[j].lower()
                if "tarjous" in kap:
                    alennukset = alennukset + "{} {}\n".format(items[j],dap[j]) + "\n"

            osoite1 = tree2.xpath('//div[@class="listpager"]/ul/li/a/@href')

            try:
                page3 = requests.get('https://www.jimms.fi{}{}'.format(c,osoite1[0]))
            except IndexError:
                pass
            while(True):
                try:
                    tree3 = html.fromstring(page3.content)
                    items3 = tree3.xpath('//div[@class="p_col_info"]/div/a/text()') #page?2 tiedot
                    osoite1 = tree3.xpath('//div[@class="listpager"]/ul/li/a/@href')#page?3
                    joo = tree3.xpath('//div[@class="p_col_price"]/div/text()')
                    kap = []

                    for i in joo:
                        if(len(i)>46):
                            kap.append(re.sub(' +',' ',i).strip('\r\n '))
                        else:
                            pass
                    for s in range(len(items3)):
                        kas = items3[s].lower()
                        if "tarjous" in kas:
                            alennukset = alennukset + "{} {}\n".format(items3[s],kap[s]) + "\n"




                    page3 = requests.get('https://www.jimms.fi{}{}'.format(c,osoite1[1])) #page?2
                except IndexError:
                    break

    return alennukset
print(itsefunktio())
