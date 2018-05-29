# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.select import Select


class AutomateDriver(object):
    """
    a simple demo of selenium framework tool
    """
    #构造函数，打开火狐浏览器
    def __init__(self, driver):
        self.driver = driver

    #清除Cookie
    def clear_cookies(self):
        """
        clear all cookies after driver init
        """
        self.driver.delete_all_cookies()

    #刷新浏览器
    def refresh_browser(self):
        self.driver.refresh()

    #最大化浏览器
    def maximize_window(self):
        self.driver.maximize_window()

    #浏览器中导航打开一个URL
    def navigate(self, url):
        """
        打开 URL
        :param url:
        :return:
        """
        self.driver.get(url)

    #退出浏览器
    def quit_browser(self):
        self.driver.quit()

    #关闭浏览器页
    def close_browser(self):
        self.driver.close()

    #根据参数从当前浏览器中定位一个元素
    def get_element(self, selector):
        """
        to locate element by selector
        :arg
        selector should be passed by an example with "i,xxx"
        "x,//*[@id='langs']/button"
        :returns
        DOM element
        """
        if ',' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split(',')[0]
        selector_value = selector.split(',')[1]

        if selector_by == "i" or selector_by == 'id':
            element = self.driver.find_element_by_id(selector_value)
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            element = self.driver.find_element_by_xpath(selector_value)
        elif selector_by == "s" or selector_by == 'css_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    #根据参数从当前浏览器中定位一组元素
    def get_elements(self, selector):
        """
        to locate element by selector
        :arg
        selector should be passed by an example with "i,xxx"
        "x,//*[@id='langs']/button"
        :returns
        DOM element
        """
        if ',' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split(',')[0]
        selector_value = selector.split(',')[1]

        if selector_by == "i" or selector_by == 'id':
            elements = self.driver.find_elements_by_id(selector_value)
        elif selector_by == "n" or selector_by == 'name':
            elements = self.driver.find_elements_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            elements = self.driver.find_elements_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            elements = self.driver.find_elements_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            elements = self.driver.find_elements_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            elements = self.driver.find_elements_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            elements = self.driver.find_elements_by_xpath(selector_value)
        elif selector_by == "s" or selector_by == 'css_selector':
            elements = self.driver.find_elements_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return elements

    #往页面元素中输入文本（输入框）
    def type(self, selector, text):
        """
        Operation input box.

        Usage:
        driver.type("i,el","selenium")
        """
        el = self.get_element(selector)
        el.clear()
        el.send_keys(text)

    def type_d(self, selector, text):
        """
        Operation input box.

        Usage:
        driver.type_d("i,el","selenium")
        """
        if text != "#d#":
            self.type(selector, text)

    #点击一个页面元素（按钮，链接等）
    def click(self, selector):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("i,el")
        """
        el = self.get_element(selector)
        #点击如果出错，需要点击两次，排除了selenium中不稳定的因素
        try:
            el.click()
        except Exception as e:
            el.click()

    #下拉列表元素按照序号选择一个选项
    def select_by_index(self, selector, index):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self.get_element(selector)
        Select(el).select_by_index(index)


    #下拉列表元素按照可见的文本选择一个选项
    def select_by_visible_text(self, selector, text):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self.get_element(selector)
        try:
            Select(el).select_by_visible_text(text)
        except Exception as e:
            Select(el).select_by_visible_text(text.lower())

    #下拉列表元素按照可见的文本选择一个选项
    def select_by_visible_text_d(self, selector, text):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_visible_text_d("i,el", text)
        """
        if text != "#d#":
            self.select_by_visible_text(selector, text)

    #下拉列表元素按照列表值选择一个元素
    def select_by_value(self, selector, value):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self.get_element(selector)
        Select(el).select_by_value(value)

    #点击页面中的任意链接文字
    def click_by_text(self, text):
        """
        Click the element by the link text

        Usage:
        driver.click_text("新闻")
        """
        self.get_element('p,' + text).click()

    #提交一个指定的form
    def submit(self, selector):
        """
        Submit the specified form.

        Usage:
        driver.submit("i,el")
        """
        el = self.get_element(selector)
        el.submit()

    #执行一段js代码
    def execute_js(self, script):
        """
        Execute JavaScript scripts.

        Usage:
        driver.js("window.scrollTo(200,1000);")
        """
        self.driver.execute_script(script)

    #获取指定元素的一个属性的值
    def get_attribute(self, selector, attribute):
        """
        Gets the value of an element attribute.

        Usage:
        driver.get_attribute("i,el","type")
        """
        el = self.get_element(selector)
        return el.getAttribute(attribute)

    #获取指定元素的文本内容
    def get_text(self, selector):
        """
        Get element text information.

        Usage:
        driver.get_text("i,el")
        """
        el = self.get_element(selector)
        return el.text

    #获取指定元素是否当前在页面显示，返回值为True / False
    def get_display(self, selector):
        """
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("i,el")
        """
        el = self.get_element(selector)
        return el.is_displayed()

    #获取页面的标题
    def get_title(self):
        '''
        Get window title.

        Usage:
        driver.get_title()
        '''
        return self.driver.title

    #获取当前浏览器页面的URL
    def get_url(self):
        """
        Get the URL address of the current page.

        Usage:
        driver.get_url()
        """
        return self.driver.current_url

    #JS提示框点确定
    def accept_alert(self):
        '''
            Accept warning box.

            Usage:
            driver.accept_alert()
            '''
        self.driver.switch_to.alert.accept()

    #JS提示框点取消
    def dismiss_alert(self):
        '''
        Dismisses the alert available.

        Usage:
        driver.dismissAlert()
        '''
        self.driver.switch_to.alert.dismiss()

    #隐式等待
    def implicitly_wait(self, secs):
        """
        Implicitly wait. All elements on the page.

        Usage:
        driver.implicitly_wait(10)
        """
        self.driver.implicitly_wait(secs)

    #切换到一个frame
    def switch_frame(self, selector):
        """
        Switch to the specified frame.

        Usage:
        driver.switch_to_frame("i,el")
        """
        el = self.get_element(selector)
        self.driver.switch_to.frame(el)

    #切换到一个默认的frame,即最上一层
    def switch_default_frame(self):
        """
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        driver.switch_to_frame_out()
        """
        self.driver.switch_to.default_content()

    #打开一个新的浏览器窗口
    def open_new_window(self, selector):
        '''
        Open the new window and switch the handle to the newly opened window.

        Usage:
        driver.open_new_window()
        '''
        original_windows = self.driver.current_window_handle
        el = self.get_element(selector)
        el.click()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_windows:
                self.driver._switch_to.window(handle)
