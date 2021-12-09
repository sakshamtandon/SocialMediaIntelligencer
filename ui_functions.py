from __future__ import unicode_literals

from reportlab.pdfbase.ttfonts import TTFont

from inscrawler import InsCrawler
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pyautogui import click
from selenium import webdriver
from bs4 import BeautifulSoup as bs, BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import re
import pdfkit as pdf
from fpdf import FPDF
import tweepy
import random
import urllib
from selenium import webdriver
import csv
import datetime
import argparse
import time
import json
import csv
import requests
import sys
import os
import pandas as pd
import argparse
import json
import sys
from io import open
from textblob import TextBlob

from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
## ==> GUI FILE
from main import *

## ==> GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

## ==> COUT INITIAL MENU
count = 1


class UIFunctions(MainWindow):
    ## ==> GLOBALS
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    ########################################################################
    ## START - GUI FUNCTIONS
    ########################################################################

    ## ==> MAXIMIZE/RESTORE
    ########################################################################

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            # self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            # self.ui.frame_size_grip.show()

    ## ==> RETURN STATUS
    def returStatus(self):
        return GLOBAL_STATE

    ## ==> SET STATUS
    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    ## ==> ENABLE MAXIMUM SIZE
    ########################################################################
    def enableMaximumSize(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()

    ## ==> TOGGLE MENU
    ########################################################################
    def toggleMenu(self, maxWidth, enable):
        if enable:
            # GET WIDTH
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    ## ==> SET TITLE BAR
    ########################################################################
    def removeTitleBar(status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    ## ==> HEADER TEXTS
    ########################################################################
    # LABEL TITLE
    def labelTitle(self, text):
        self.ui.label_title_bar_top.setText(text)

    # LABEL DESCRIPTION

    ## ==> DYNAMIC MENUS
    ########################################################################
    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(str(count), self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)

    ## ==> SELECT/DESELECT MENU
    ########################################################################
    ## ==> SELECT
    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    ## ==> DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    ## ==> START SELECTION
    # def selectStandardMenu(self, widget):
    #     for w in self.ui.frame_left_menu.findChildren(QPushButton):
    #         if w.objectName() == widget:
    #             w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    ## ==> RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    ## ==> CHANGE PAGE LABEL TEXT
    def labelPage(self, text):
        newText = '| ' + text.upper()
        self.ui.label_top_info_2.setText(newText)

    ## ==> USER ICON
    ########################################################################
    def userIcon(self, initialsTooltip, icon, showHide):
        if showHide:
            # SET TEXT
            self.ui.label_user_icon.setText(initialsTooltip)

            # SET ICON
            if icon:
                style = self.ui.label_user_icon.styleSheet()
                setIcon = "QLabel { background-image: " + icon + "; }"
                self.ui.label_user_icon.setStyleSheet(style + setIcon)
                self.ui.label_user_icon.setText('')
                self.ui.label_user_icon.setToolTip(initialsTooltip)
        else:
            self.ui.label_user_icon.hide()

    def addbutton_click(self):
        keyword = self.ui.lineEdit_keyword.text()
        count = self.ui.lineEdit_count.text()

    def instagram_scraper_click(self):
        counter = 1

        self.ui.progressBar.setValue(counter)
        while (counter < random.randint(2, 12)):
            time.sleep(1)
            self.ui.progressBar.setValue(counter)
            counter += 1
        keyword = self.ui.lineEdit_keyword.text()
        count = self.ui.lineEdit_count.text()
        keyword = keyword.replace(' ', '')

        def get_posts_by_hashtag(KEYWORD, COUNT, debug):
            ins_crawler = InsCrawler(has_screen=debug)
            return ins_crawler.get_latest_posts_by_tag(KEYWORD, COUNT)

        def output(data, filepath):
            out = json.dumps(data, ensure_ascii=False)  # Converts a Python object into a json string.
            if filepath:
                with open(filepath + ".json", "w", encoding="utf8") as f:
                    f.write(out)
            else:
                print(out)

        def usage():
            return """
            """

        parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())
        optional_parser = parser.add_argument_group("optional arguments")
        optional_parser.add_argument("-n", "--number", type=int, help="number of returned posts")
        optional_parser.add_argument("-u", "--username", help="instagram's username")

        optional_parser.add_argument("-t", "--tag", help="instagram's tag name")
        optional_parser.add_argument("-o", "--output", help="output file name(json format)")
        optional_parser.add_argument("--debug", action="store_true")

        prepare_override_settings(parser)

        args = parser.parse_args()

        override_settings(args)

        output(get_posts_by_hashtag(keyword, int(count), args.debug), "./output")

        df = pd.read_json(r'output.json', encoding='utf-8')
        df['Source'] = 'Instagram'
        df.rename(columns={'key': 'PostLink', 'caption': 'post', 'img_url': 'Image_Link'}, inplace=True)
        cols = list(df.columns)
        cols = [cols[-1]] + cols[:-1]
        df = df[cols]
        df.insert(1, 'profile', df['post'])
        df.insert(5, 'Location', 'NA')

        print(df)
        df.to_sql("master", conn, if_exists='append', index=False)
        while (counter < 101):
            self.ui.progressBar.setValue(counter)
            counter += 4
        self.ui.progressBar.setValue(100)
        # export_csv = df.to_csv(keyword + '.csv', index=None, header=True)

    def facebook_scraper_click(self):
        counter = 0
        self.ui.progressBar.setValue(counter)
        while (counter < 6):
            time.sleep(1)
            self.ui.progressBar.setValue(counter)
            counter += 1
        with open('facebook_credentials.txt') as file:
            EMAIL = file.readline().split('"')[1]
            PASSWORD = file.readline().split('"')[1]

        KEYWORD = self.ui.lineEdit_keyword.text()
        COUNT = self.ui.lineEdit_count.text()

        def _extract_post_text(item):
            actualPosts = item.find_all(class_="a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7")
            text = ""
            for actualPost in actualPosts:
                text = actualPost.get_text()
                # print(text)
            text.encode('utf-8')

            return text

        def _extract_link(item):
            postLinks = item.find_all(
                class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p dkezsu63")

            link = ""
            for postLink in postLinks:
                link = postLink.get('href')
                # print(link)

            return link

        def _extract_post_id(item):
            postIds = item.find_all(
                class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 a8c37x1j p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l")
            post_id = ""
            for postId in postIds:
                try:
                    # "https://www.facebook.com" +
                    post_id = f"{postId.get('href')}"
                    # print(post_id)
                except:
                    post_id = "NA"

            return post_id

        def _extract_image(item):
            postPictures = item.find_all(class_="a8c37x1j bixrwtb6")
            image = ""
            for postPicture in postPictures:
                image = postPicture.get('src')
                # print(image)

            return image

        def _extract_shares(item):
            postShares = item.find_all(class_="_4vn1")
            shares = ""
            for postShare in postShares:

                x = postShare.string
                if x is not None:
                    x = x.split(">", 1)
                    shares = x
                else:
                    shares = "0"
            return shares

        def _extract_comments(item):
            postComments = item.findAll("div", {"class": "_4eek"})
            comments = dict()
            # print(postDict)
            for comment in postComments:
                if comment.find(class_="_6qw4") is None:
                    continue

                commenter = comment.find(class_="_6qw4").text
                comments[commenter] = dict()

                comment_text = comment.find("span", class_="_3l3x")

                if comment_text is not None:
                    comments[commenter]["text"] = comment_text.text

                comment_link = comment.find(class_="_ns_")
                if comment_link is not None:
                    comments[commenter]["link"] = comment_link.get("href")

                comment_pic = comment.find(class_="_2txe")
                if comment_pic is not None:
                    comments[commenter]["image"] = comment_pic.find(class_="img").get("src")

                commentList = item.find('ul', {'class': '_7791'})
                if commentList:
                    comments = dict()
                    comment = commentList.find_all('li')
                    if comment:
                        for litag in comment:
                            aria = litag.find("div", {"class": "_4eek"})
                            if aria:
                                commenter = aria.find(class_="_6qw4").text
                                comments[commenter] = dict()
                                comment_text = litag.find("span", class_="_3l3x")
                                if comment_text:
                                    comments[commenter]["text"] = comment_text.text
                                    # print(str(litag)+"\n")

                                comment_link = litag.find(class_="_ns_")
                                if comment_link is not None:
                                    comments[commenter]["link"] = comment_link.get("href")

                                comment_pic = litag.find(class_="_2txe")
                                if comment_pic is not None:
                                    comments[commenter]["image"] = comment_pic.find(class_="img").get("src")

                                repliesList = litag.find(class_="_2h2j")
                                if repliesList:
                                    reply = repliesList.find_all('li')
                                    if reply:
                                        comments[commenter]['reply'] = dict()
                                        for litag2 in reply:
                                            aria2 = litag2.find("div", {"class": "_4efk"})
                                            if aria2:
                                                replier = aria2.find(class_="_6qw4").text
                                                if replier:
                                                    comments[commenter]['reply'][replier] = dict()

                                                    reply_text = litag2.find("span", class_="_3l3x")
                                                    if reply_text:
                                                        comments[commenter]['reply'][replier][
                                                            "reply_text"] = reply_text.text

                                                    r_link = litag2.find(class_="_ns_")
                                                    if r_link is not None:
                                                        comments[commenter]['reply']["link"] = r_link.get("href")

                                                    r_pic = litag2.find(class_="_2txe")
                                                    if r_pic is not None:
                                                        comments[commenter]['reply']["image"] = r_pic.find(
                                                            class_="img").get("src")
            return comments

        def _extract_reaction(item):
            toolBar = item.find_all(attrs={"role": "toolbar"})

            if not toolBar:  # pretty fun
                return
            reaction = dict()
            for toolBar_child in toolBar[0].children:
                str = toolBar_child['data-testid']
                reaction = str.split("UFI2TopReactions/tooltip_")[1]

                reaction[reaction] = 0

                for toolBar_child_child in toolBar_child.children:

                    num = toolBar_child_child['aria-label'].split()[0]

                    # fix weird ',' happening in some reaction values
                    num = num.replace(',', '.')

                    if 'K' in num:
                        realNum = float(num[:-1]) * 1000
                    else:
                        realNum = float(num)

                    reaction[reaction] = realNum
            return reaction

        def _extract_html(bs_data):

            # Add to check
            with open('./bs.html', "w", encoding="utf-8") as file:
                file.write(str(bs_data.prettify()))

            k = bs_data.find_all(
                class_="rq0escxv l9j0dhe7 du4w35lb hybvsw6c ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi ni8dbmo4 stjgntxs k4urcfbm sbcfpzgs")
            postBigDict = list()

            for item in k:
                postDict = dict()
                postDict['Post'] = _extract_post_text(item)
                postDict['Link'] = _extract_link(item)
                postDict['PostId'] = _extract_post_id(item)
                postDict['Image'] = _extract_image(item)
                postDict['Shares'] = _extract_shares(item)
                postDict['Comments'] = _extract_comments(item)
                # postDict['Reaction'] = _extract_reaction(item)

                # Add to check
                postBigDict.append(postDict)
                with open('./postBigDict.json', 'w', encoding='utf-8') as file:
                    file.write(json.dumps(postBigDict, ensure_ascii=False).encode('utf-8').decode())

            return postBigDict

        def _login(browser, email, password):
            browser.get("http://facebook.com")
            browser.maximize_window()
            browser.find_element_by_name("email").send_keys(email)
            browser.find_element_by_name("pass").send_keys(password)

            # Facebook new design
            browser.find_element_by_name("login").click()

            time.sleep(15)

        def _search(browser, page):

            if (len(self.ui.lineEdit.text()) != 0):
                LOCATION = self.ui.lineEdit.text()
                url = "https://www.facebook.com/search/posts/?q=" + page + "&filters=eyJycF9hdXRob3IiOiJ7XCJuYW1lXCI6XCJtZXJnZWRfcHVibGljX3Bvc3RzXCIsXCJhcmdzXCI6XCJcIn0ifQ%3D%3D"
                browser.get(url)
                time.sleep(5)
                browser.find_element_by_xpath(
                    '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/div[4]/div/div/div/div/div/div/div[1]/div/div[2]/i').click()
                actions = ActionChains(browser)
                actions.send_keys(LOCATION)
                actions.perform()
                time.sleep(10)



            else:
                url = "https://www.facebook.com/search/posts/?q=" + page + "&filters=eyJycF9hdXRob3IiOiJ7XCJuYW1lXCI6XCJtZXJnZWRfcHVibGljX3Bvc3RzXCIsXCJhcmdzXCI6XCJcIn0ifQ%3D%3D"
                browser.get(url)
                time.sleep(5)

        def _count_needed_scrolls(browser, infinite_scroll, numOfPost):
            if infinite_scroll:
                lenOfPage = browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
                )
            else:
                # roughly 8 post per scroll kindaOf
                lenOfPage = int(numOfPost / 8)
            print("Number Of Scrolls Needed " + str(lenOfPage))
            return lenOfPage

        def _scroll(browser, infinite_scroll, lenOfPage):
            lastCount = -1
            match = False

            while not match:
                if infinite_scroll:
                    lastCount = lenOfPage
                else:
                    lastCount += 1

                # wait for the browser to load, this time can be changed slightly ~3 seconds with no difference, but 5 seems
                # to be stable enough
                time.sleep(5)

                if infinite_scroll:
                    lenOfPage = browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                        "lenOfPage;")
                else:
                    browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                        "lenOfPage;")

                if lastCount == lenOfPage:
                    match = True

        def extract(page, numOfPost, infinite_scroll=False, scrape_comment=False):
            option = Options()
            option.add_argument("--disable-infobars")
            # option.add_argument("--headless")
            option.add_argument('--user-data-dir=./User_Data')
            option.add_argument("start-maximized")
            option.add_argument("--disable-extensions")
            # option.add_extension("Old Layout for Facebook.crx")
            # Pass the argument 1 to allow and 2 to block
            option.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 1
            })

            # chromedriver should be in the same folder as file
            browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)
            # browser= webdriver.Chrome(executable_path="./chromedriver", options=option)
            try:
                _login(browser, EMAIL, PASSWORD)
            except:
                pass
            _search(browser, page)
            lenOfPage = _count_needed_scrolls(browser, infinite_scroll, numOfPost)
            _scroll(browser, infinite_scroll, lenOfPage)

            # click on all the comments to scrape them all!
            # TODO: need to add more support for additional second level comments
            # TODO: ie. comment of a comment

            if scrape_comment:
                # first uncollapse collapsed comments
                unCollapseCommentsButtonsXPath = '//a[contains(@class,"_666h")]'
                unCollapseCommentsButtons = browser.find_elements_by_xpath(unCollapseCommentsButtonsXPath)
                for unCollapseComment in unCollapseCommentsButtons:
                    action = webdriver.common.action_chains.ActionChains(browser)
                    try:
                        # move to where the un collapse on is
                        action.move_to_element_with_offset(unCollapseComment, 5, 5)
                        action.perform()
                        unCollapseComment.click()
                    except:
                        # do nothing right here
                        pass

                # second set comment ranking to show all comments
                rankDropdowns = browser.find_elements_by_class_name('sjgh65i0')  # select boxes who have rank dropdowns
                rankXPath = '//div[contains(concat(" ", @class, " "), "uiContextualLayerPositioner") and not(contains(concat(" ", @class, " "), "hidden_elem"))]//div/ul/li/a[@class="_54nc"]/span/span/div[@data-ordering="RANKED_UNFILTERED"]'
                for rankDropdown in rankDropdowns:
                    # click to open the filter modal
                    action = webdriver.common.action_chains.ActionChains(browser)
                    try:
                        action.move_to_element_with_offset(rankDropdown, 5, 5)
                        action.perform()
                        rankDropdown.click()
                    except:
                        pass

                    # if modal is opened filter comments
                    ranked_unfiltered = browser.find_elements_by_xpath(rankXPath)  # RANKED_UNFILTERED => (All Comments)
                    if len(ranked_unfiltered) > 0:
                        try:
                            ranked_unfiltered[0].click()
                        except:
                            pass

                moreComments = browser.find_elements_by_xpath('//a[@class="_4sxc _42ft"]')
                print("Scrolling through to click on more comments")
                while len(moreComments) != 0:
                    for moreComment in moreComments:
                        action = webdriver.common.action_chains.ActionChains(browser)
                        try:
                            # move to where the comment button is
                            action.move_to_element_with_offset(moreComment, 5, 5)
                            action.perform()
                            moreComment.click()
                        except:
                            # do nothing right here
                            pass

                    moreComments = browser.find_elements_by_xpath('//a[@class="_4sxc _42ft"]')

            # Now that the page is fully scrolled, grab the source code.
            source_data = browser.page_source

            # Throw your source into BeautifulSoup and start parsing!
            bs_data = bs(source_data, 'html.parser')

            postBigDict = _extract_html(bs_data)
            browser.close()

            return postBigDict

        parser = argparse.ArgumentParser(description="Facebook Page Scraper")
        required_parser = parser.add_argument_group("required arguments")
        # required_parser.add_argument('-page', '-p', help="The Facebook Public Page you want to scrape", required=True)
        # required_parser.add_argument('-len', '-l', help="Number of Posts you want to scrape", type=int, required=True)
        optional_parser = parser.add_argument_group("optional arguments")
        optional_parser.add_argument('-infinite', '-i',
                                     help="Scroll until the end of the page (1 = infinite) (Default is 0)", type=int,
                                     default=0)
        optional_parser.add_argument('-usage', '-u', help="What to do with the data: "
                                                          "Print on Screen (PS), "
                                                          "Write to Text File (WT) (Default is WT)", default="CSV")

        optional_parser.add_argument('-comments', '-c', help="Scrape ALL Comments of Posts (y/n) (Default is n). When "
                                                             "enabled for pages where there are a lot of comments it can "
                                                             "take a while", default="No")
        args = parser.parse_args()

        infinite = False
        if args.infinite == 1:
            infinite = True

        scrape_comment = False
        if args.comments == 'y':
            scrape_comment = True

        postBigDict = extract(KEYWORD, int(COUNT), infinite_scroll=infinite, scrape_comment=scrape_comment)

        # TODO: rewrite parser
        if args.usage == "WT":
            with open('output.txt', 'w') as file:
                for post in postBigDict:
                    file.write(json.dumps(post))  # use json load to recover

        elif args.usage == "CSV":
            source = "Facebook"

            if (len(self.ui.lineEdit.text()) != 0):
                LOCATION = self.ui.lineEdit.text()
                for post in postBigDict:
                    c.execute(
                        '''INSERT INTO master(Source, Profile,Post , PostLink ,Image_Link ,Location  ) VALUES(?,?,?,?,?,?)''',
                        (source, post['Link'], post['Post'], post['PostId'], post['Image'], LOCATION))

                    # writer.writerow([post['PostId'], post['Link'], post['Post'], post['Image']])
                    # writer.writerow([post['Post'], post['Link'],post['Image'], post['Comments'], post['Reaction']])

            else:
                for post in postBigDict:
                    c.execute(
                        '''INSERT INTO master(Source, Profile,Post , PostLink ,Image_Link ,Location  ) VALUES(?,?,?,?,?,?)''',
                        (source, post['Link'], post['Post'], post['PostId'], post['Image'], "NA"))

                    # writer.writerow([post['PostId'], post['Link'], post['Post'], post['Image']])
                    # writer.writerow([post['Post'], post['Link'],post['Image'], post['Comments'], post['Reaction']])

                conn.commit()


        else:
            for post in postBigDict:
                print(post.encode("utf-8"))

        while (counter < 101):
            self.ui.progressBar.setValue(counter)
            counter += 4
        self.ui.progressBar.setValue(100)

    def twitter_scraper_click(self):
        counter = 0
        self.ui.progressBar.setValue(counter)
        while (counter < 6):
            time.sleep(1)
            self.ui.progressBar.setValue(counter)
            counter += 1
        with open('twitter_credentials.txt') as file:
            consumer_key = file.readline().split('"')[1]
            consumer_secret = file.readline().split('"')[1]
            access_key = file.readline().split('"')[1]
            access_secret = file.readline().split('"')[1]
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # Access to user's access key and access secret
        auth.set_access_token(access_key, access_secret)

        # Calling api
        api = tweepy.API(auth)

        KEYWORD = self.ui.lineEdit_keyword.text()
        COUNT = self.ui.lineEdit_count.text()

        def tweets_by_word_search(word):
            source = "Twitter"
            if len(self.ui.lineEdit_2.text()) != 0:
                GEOCODE = self.ui.lineEdit_2.text()
                for tweet in tweepy.Cursor(api.search, q=word, lang='en', geocode=GEOCODE).items(int(COUNT)):
                    tweets_encoded = tweet.text.encode('utf-8')
                    tweets_decoded = tweets_encoded.decode('utf-8')
                    c.execute(
                        '''INSERT INTO master(Source, Profile,Post , PostLink ,Image_Link ,Location  ) VALUES(?,?,?,
                        ?,?,?)''',
                        (source, tweet.author._json['screen_name'].encode("utf-8"), tweets_decoded.encode("utf-8"),
                         "https://twitter.com/i/web/status/" + str(tweet.id), "NA",
                         str(tweet._json["user"]["location"]) + " " + str(tweet.created_at)))

            else:
                for tweet in tweepy.Cursor(api.search, q=word, lang='en').items(int(COUNT)):
                    tweets_encoded = tweet.text.encode('utf-8')
                    tweets_decoded = tweets_encoded.decode('utf-8')
                    c.execute(
                        '''INSERT INTO master(Source, Profile,Post , PostLink ,Image_Link ,Location  ) VALUES(?,?,?,?,?,?)''',
                        (source, tweet.author._json['screen_name'].encode("utf-8"), tweets_decoded,
                         "https://twitter.com/i/web/status/" + str(tweet.id), "NA",
                         str(tweet._json["user"]["location"]) + " " + str(tweet.created_at)))

            conn.commit()

        tweets_by_word_search(KEYWORD)

        while counter < 101:
            self.ui.progressBar.setValue(counter)
            counter += 1

    def youtube_scraper_click(self):
        counter = 0
        self.ui.progressBar.setValue(counter)
        while (counter < 6):
            time.sleep(1)
            self.ui.progressBar.setValue(counter)
            counter += 1

        KEYWORD = self.ui.lineEdit_keyword.text()
        base_url = "https://www.youtube.com/"

        def scrap():
            scrap_each_query(KEYWORD)

        def scrap_each_query(keyword):
            real_keyword = keyword
            keyword = urllib.parse.quote(urllib.parse.quote(keyword))
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

            for i in range(1):
                url = base_url + "results?search_query=" + real_keyword
                driver.get(url)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                content = soup.findAll("div", {"class": "text-wrapper style-scope ytd-video-renderer"})
                base_url1 = "https://www.youtube.com"
                source = "Youtube"
                for each in content:
                    all_content = each.find("yt-formatted-string",
                                            {"class": "style-scope ytd-video-renderer"}).get_text().encode('utf-8')
                    all_name = each.find("a",
                                         {"class": "yt-simple-endpoint style-scope yt-formatted-string"}).get_text()
                    all_link = base_url1 + each.find("a", {
                        "class": "yt-simple-endpoint style-scope yt-formatted-string"}).get("href")
                    all_link1 = base_url1 + each.find("a", {
                        "class": "yt-simple-endpoint style-scope ytd-video-renderer"}).get("href")
                    c.execute(
                        '''INSERT INTO master(Source, Profile,Post , PostLink ,Image_Link ,Location  ) VALUES(?,?,?,?,?,?)''',
                        (source, all_name, all_content, all_link1, all_link, "NA"))
                driver.close()
                conn.commit()

        scrap()

        while (counter < 101):
            self.ui.progressBar.setValue(counter)
            counter += 1

    def other_scraper_click(self):
        counter = 0
        self.ui.progressBar.setValue(counter)
        while (counter < 6):
            time.sleep(1)
            self.ui.progressBar.setValue(counter)
            counter += 1

        KEYWORD = self.ui.lineEdit_keyword.text()

        base_url = 'https://www.google.com/'

        def scrap():
            scrap_each_query(KEYWORD)

        def scrap_each_query(keyword):
            keyword = urllib.parse.quote(urllib.parse.quote(keyword))
            keyword = keyword.replace('%2520', '+')
            all_heading = []
            all_heading_link = []
            all_content = []

            co = webdriver.ChromeOptions()
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=co)

            url = "https://www.google.com/"
            driver.get(url)
            url = base_url + "search?q=intext:" + keyword + "+intitle:news&start=0"
            driver.get(url)

            time.sleep(100)

            for i in range(int(3)):

                url = base_url + "search?q=intext:" + keyword + "+intitle:news&start=" + str(i + 10)
                driver.get(url)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                heading = soup.findAll("div", {"class": "g"})
                source = "Other source"

                for each in heading:
                    all_heading = each.find("h3", {"class": "LC20lb DKV0Md"}).get_text().encode('utf-8')
                    all_heading_link = each.find("div", {"class": "yuRUbf"}).a.get('href').encode('utf-8')
                    all_content = each.find("div", {"class": "IsZvec"}).get_text().encode('utf-8')

                    c.execute(
                        '''INSERT INTO master(Source, Profile,Post , PostLink ,Image_Link ,Location  ) VALUES(?,?,?,?,?,?)''',
                        (source, all_heading, all_content, all_heading_link, "NA", "NA"))

                url = base_url + "search?q=intext:" + keyword + "+intitle:blogs&start=" + str(i + 10)
                driver.get(url)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                heading = soup.findAll("div", {"class": "g"})
                source = "Other source"

                for each in heading:
                    try:
                        all_heading = each.find("h3", {"class": "LC20lb DKV0Md"}).get_text().encode('utf-8')
                        all_heading_link = each.find("div", {"class": "yuRUbf"}).a.get('href').encode('utf-8')
                        all_content = each.find("div", {"class": "IsZvec"}).get_text().encode('utf-8')

                        c.execute(
                            '''INSERT INTO master(Source, Profile,Post , PostLink ,Image_Link ,Location  ) VALUES(?,?,?,?,?,?)''',
                            (source, all_heading, all_content, all_heading_link, "NA", "NA"))
                    except:
                        pass

            driver.close()
            conn.commit()

        scrap()

        while (counter < 101):
            self.ui.progressBar.setValue(counter)
            counter += 1

    def click(self):
        # c.execute('''SELECT * FROM master''')
        result = c.execute('''SELECT * FROM master''')
        self.ui.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.ui.tableWidget.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    def clear_all(self):
        self.ui.tableWidget.setRowCount(0)
        c.execute('''DELETE FROM master''')
        conn.commit()

    def truncate_master(self):
        c.execute('''DROP TABLE master''')
        conn.commit()

    def save_to_CSV(self):
        # result = c.execute("SELECT * FROM master")
        db_df = pd.read_sql_query("SELECT * FROM master", conn)
        db_df.to_csv('database.csv', index=False)

    def save_to_pdf(self):
        counter = 0
        self.ui.progressBar.setValue(counter)
        while (counter < 3):
            self.ui.progressBar.setValue(counter)
            counter += 1

        db_df = pd.read_sql_query("SELECT * FROM master", conn)
        num = db_df.shape[0]

        post = pd.read_sql_query("SELECT * FROM master", conn)
        mentions = post.shape[0]

        def clean_tweets(tweet):
            tweet = re.sub("http\S+", "", str(tweet))
            tweet = re.sub("@[A-Za-z0-9]+", '', str(tweet))
            tweet = re.sub('[^ a-zA-Z0-9]', '', str(tweet))
            tweet = re.sub('[0-9]', '', str(tweet))  # remove Numbers
            tweet = re.sub('RT[\s]+', '', str(tweet))
            tweet = re.sub('#', '', str(tweet))
            tweet = re.sub('Photo by\S+', '', str(tweet))
            tweet = re.sub(': ', '', str(tweet))
            tweet = re.sub('[0-9]', '', str(tweet))

            return tweet

        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity

        def getPolarity(text):
            return TextBlob(text).sentiment.polarity

        def getAnalysis(score):
            if score < 0:
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'

        post['Post'] = post['Post'].apply(clean_tweets)
        post['Subjectivity'] = post['Post'].apply(getSubjectivity)
        post['Polarity'] = post['Post'].apply(getPolarity)
        post['Analysis'] = post['Polarity'].apply(getAnalysis)

        Instagram_count = len(post[post.Source == 'Instagram'])
        Facebook_count = len(post[post.Source == 'Facebook'])
        Youtube_count = len(post[post.Source == 'Youtube'])
        Other_source_count = len(post[post.Source == 'Other source'])
        Twitter_count = len(post[post.Source == 'Twitter'])

        ptweets = post[post.Analysis == 'Positive']
        ptweets.to_csv('Positive_posts.csv', index=False)
        ptweets = ptweets['Post']

        ntweets = post[post.Analysis == 'Negative']
        ntweets.to_csv('Negative_posts.csv', index=False)
        ntweets = ntweets['Post']

        nntweets = post[post.Analysis == 'Neutral']
        nntweets = nntweets['Post']

        allWords = ' '.join([twts for twts in post['Post']])
        wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
        wordCloud = wordCloud.to_file('wordcloud.png')

        canvas = Canvas('output.pdf')
        # watermark = "watermark.png"
        wordcloud = "wordcloud.png"
        head = "SOCIAL MEDIA MONITOR"
        canvas.drawString(230, 750, head)
        # canvas.drawInlineImage(watermark, 170, 450, width=280, height=280)
        canvas.drawString(240, 400, "AUTOMATION REPORT")
        canvas.showPage()
        # canvas.drawInlineImage(watermark, 10, 780, width=50, height=50)
        canvas.drawString(220, 800, "SENTIMENT ANALYSIS REPORT")
        canvas.drawString(50, 750, "Total Mentioned: ")
        canvas.drawString(170, 750, str(mentions))
        canvas.drawString(50, 700, "Positive Sentiments: ")
        canvas.drawString(170, 700, str(ptweets.shape[0]))
        canvas.drawString(50, 650, "Negative Sentiments: ")
        canvas.drawString(170, 650, str(ntweets.shape[0]))
        canvas.drawString(50, 600, "Neutral Sentiments: ")
        canvas.drawString(170, 600, str(nntweets.shape[0]))
        canvas.drawString(300, 750, "Instagram Count: ")
        canvas.drawString(450, 750, str(Instagram_count))
        canvas.drawString(300, 700, "Facebook Count: ")
        canvas.drawString(450, 700, str(Facebook_count))
        canvas.drawString(300, 650, "Youtube Count: ")
        canvas.drawString(450, 650, str(Youtube_count))
        canvas.drawString(300, 600, "Other source Count: ")
        canvas.drawString(450, 600, str(Other_source_count))
        canvas.drawString(300, 550, "Twitter Count: ")
        canvas.drawString(450, 550, str(Twitter_count))
        canvas.drawString(50, 500, "WORD CLOUD CHART")
        canvas.drawInlineImage(wordcloud, 50, 150, width=500, height=300)
        canvas.showPage()

        for i in range(num):

            font = r"HindSiliguri-Regular.ttf"
            pdfmetrics.registerFont(TTFont('NotoSerif', font))
            canvas.setFont('NotoSerif', 11)

            if (i > 0):
                if (i % 4 == 0):
                    canvas.showPage()
                # img1 = image[i]
                #canvas.drawInlineImage(watermark, 10, 780, width=50, height=50)
                # canvas.drawInlineImage(img1, 30, 700 - i % 7 * 100, width=60, height=50)
                canvas.drawString(50, 750 - i % 4 * 160, "Source: ")
                canvas.drawString(100, 750 - i % 4 * 160, db_df['Source'][i])
                canvas.drawString(50, 725 - i % 4 * 160, "Profile: ")
                canvas.drawString(100, 725 - i % 4 * 160, db_df['Profile'][i])
                canvas.drawString(50, 700 - i % 4 * 160, "Post: ")
                canvas.drawString(100, 700 - i % 4 * 160, db_df['Post'][i])
                canvas.drawString(50, 675 - i % 4 * 160, "Link: ")
                canvas.setFillColorRGB(0, 0, 1)
                canvas.drawString(100, 675 - i % 4 * 160, db_df['PostLink'][i])
                canvas.setFillColorRGB(0, 0, 0)
                canvas.drawString(50, 650 - i % 4 * 160, "Other Link:")
                canvas.setFillColorRGB(0, 0, 1)
                try:
                    canvas.drawString(120, 650 - i % 4 * 160, db_df['Image_Link'][i])
                except:
                    pass
                canvas.setFillColorRGB(0, 0, 0)
                canvas.drawString(50, 625 - i % 4 * 160, "Location/Time/Date:")
                canvas.drawString(170, 625 - i % 4 * 160, db_df['Location'][i])

                # canvas.setFillColorRGB(0, 0, 1)
                # canvas.setFillColorRGB(0, 0, 0)
                canvas.drawString(50, 600 - i % 4 * 160,
                                  "---------------------******************************************************************----------------------")

        canvas.showPage()

        canvas.save()

        while (counter < 101):
            self.ui.progressBar.setValue(counter)
            counter += 8
        self.ui.progressBar.setValue(100)

    ########################################################################
    ## END - GUI FUNCTIONS
    ########################################################################

    ########################################################################
    ## START - GUI DEFINITIONS
    ########################################################################

    ## ==> UI DEFINITIONS
    ########################################################################
    def uiDefinitions(self):

        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        ## REMOVE ==> STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()

        ## SHOW ==> DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        ## ==> RESIZE WINDOW
        # self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        # self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        ### ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## ==> MAXIMIZE/RESTORE
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        ## SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())

    ########################################################################
    ## END - GUI DEFINITIONS
    ########################################################################
