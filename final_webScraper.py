# coding: utf-8
import io
import csv
import codecs
from urllib.request import urlopen as uo
from bs4 import BeautifulSoup as soup
from tkinter import *

def getURL(page):
    global containerAmount
    for counter in range(page):
        my_url = 'https://store.steampowered.com/search/?specials=1&page=' + str(counter)
        print(counter)
        
        uPage = uo(my_url)
        my_html = uPage.read()
        uPage.close()
        global pageParse
        pageParse = soup(my_html, 'html.parser')
        global myContainers
        myContainers = pageParse.find_all("div", {'class', 'responsive_search_name_combined'})
        containerAmount +=len(myContainers)
        getPNamePriceReview()
        getPlatform()
        getRating()



def getPNamePriceReview():
    #print(containerAmount)
    #---------------------------------brandName, price,
    for m in myContainers:
        s = m.text.split('\n')
        if len(s) < 19:
            DropDown_list.append(s[11])
            p1 = s[len(s)-3][0:-7].split('$')
            if len(p1) < 3:
                oriPrice_list.append(s[len(s)-3][0:-7])
                nowPrice_list.append(s[len(s)-3][0:-7])
            else:
                op = p1[1]
                np = p1[2]
                oriPrice_list.append('$' + op)
                nowPrice_list.append('$' + np)
        else:
            p1 = s[16][0:-7].split('$')
            if len(p1) < 3:
                oriPrice_list.append(s[16][0:-7])
                nowPrice_list.append(s[16][0:-7])
            else:
                op = p1[1]
                np = p1[2]
                oriPrice_list.append('$' + op)
                nowPrice_list.append('$' + np)
        # print(p)
       #object = s[2] + ',' + s[6] + ',' + s[13] + ',' + s[16][0:-7]

        #print(s[2])
        productName_list.append(s[2])
        DropDown_list.append(s[13])

def getPlatform():
       #-----------------------------------plate
    for m in myContainers:
        p2 = m.div.p
        # print('--------',p)
        pl = []
        for i in p2:
            if len(i) != 1:
                # print("------",i)
                # print("--------", len(i))
                plate = str(i)[26:29]
                pl.append(plate)
        # print('>>>>',pl)
        plate_list.append(pl)

        #-------------------------rating

def getRating():
    rateContainer = pageParse.find_all('div', {'class', 'col search_reviewscore responsive_secondrow'})
    #in order to check if I got all 25 item each page'

    if len(rateContainer) != len(myContainers):
        while len(rateContainer) != len(myContainers):
            rateContainer.append("---")

    for m in rateContainer:
       # to store percent revire and user amount
        p3 = ''
        u = ''

      
        if len(m) == 3:

            r = str(m).split(' ')
            # print(r)
            # print('))))',r)
            pr = r[6] + r[7] + r[8]
            p3 = pr[pr.index('%') - 2:pr.index('%') + 1]
            ratePercent_list.append(p3)
            user = r[9] + r[10] + r[11]

            for us in user:
                if us.isdigit():
                    u = u + us
            user_list.append(u)
            # print(p, "-------", u)
        else:
            p3 = '0%'
            ratePercent_list.append(p3)
            u = '0'
            user_list.append(u)

            # print(p,"-------",u )



#print(len(overall_reviewlist),len(ratePercent_list), len(user_list))
def writeData():
    with io.open('data.csv', "w", encoding="utf-8") as file:
        header = "Product_Name, PlatForm, Price_Down, Original_Price,Price, RatePercent, User_Amount\n"

        file.write(header)

        for j in range(0, containerAmount):
            file.write(str(productName_list[j]) + ',' + str(plate_list[j]).replace(',', '/') + ',' + str(
                DropDown_list[j]) + ',' + str(oriPrice_list[j]) + ',' + str(nowPrice_list[j]) + ',' + str(
                ratePercent_list[j]) + ',' + str(user_list[j]) + '\n')
            print(productName_list[j], plate_list[j], DropDown_list[j], oriPrice_list[j], nowPrice_list[j],
                  ratePercent_list[j], user_list[j])
        
        file.close()

class urlEntry(Entry):
    def __init__(self, master=None):
        super().__init__( master)
        self['bd'] = 5
        self['width'] = 60
        self.delete(0, END)
        self.insert(0, 'https://store.steampowered.com/search/?specials=1&page=')


def getState():
    inPage = v.get()
    lb.insert(1, '----------------------------------------------')
    getURL(inPage)
    writeData()
    disPlayData()



def disPlayData():
    lb.delete(0,END)
    
    # in case some chinese character can't not be read
    #.csv reading file and writing file can be the same name?
    f = codecs.open("data.csv", "r", "utf-8")
    
    spamreader = csv.reader(f, delimiter='|', quotechar='|')
    for row in spamreader:
        lb.insert(END, ',  '.join(row))
    
    print(len(productName_list), len(plateForm_list), len(DropDown_list), len(oriPrice_list), len(nowPrice_list),
          len(ratePercent_list), len(user_list))


#print(len(productName_list),len(plate_list),len(DropDown_list),len(oriPrice_list),len(nowPrice_list ),len(ratePercent_list),len(user_list))
#print(containerAmount)
if __name__ == '__main__':
    root = Tk()
    root.title(' My web scraper ')
    frame = Frame(root)
    v = IntVar()
    pL = Label(root, text=' Range(<30)', width=10).grid(row=0, sticky='e')
    uL = Label(root, text=' URL', width=10).grid(row=0, sticky='w')
    uE = urlEntry(root)
    uPE = Entry(root, width=10, textvariable = v)
    uPE.grid(row=0,column = 1, sticky = 'w')
    
    uE.grid(row = 0, column = 0,sticky = 's')
    lb = Listbox(root, width = 120)
    lb.insert(1,'***************************Data show here****************')
    lb.grid(row = 2,column = 0, rowspan = 2, sticky = 'nswe')
    scoll = Scrollbar(root, orient = VERTICAL)
    lb['yscrollcommand'] = scoll.set
    scoll['command'] = lb.yview
    scoll.grid(row = 2, column = 0, rowspan = 2, sticky = 'nse')
    
    Button(root, text='Go', command=getState).grid(row = 1,column = 1)
    frame.grid(row = 1)
    
    productName_list = []
    DropDown_list = []
    oriPrice_list = []
    nowPrice_list = []
    plateForm_list = []
    ratePercent_list = []
    user_list = []
    
    containerAmount = 0
    
    
    root.mainloop()
