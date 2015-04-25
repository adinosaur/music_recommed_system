#encoding=utf8
    
"""
分页助手

"""
class Page_Assistant:

    
    def __init__(self, count, page_size=10, page_list_size=10):
        """
        page_size:每张页面一共有多少个对象
        page_list_size:每个页面底部显示多少个其它页面的链接
        """
        self.count = count
        self.page_size = page_size
        self.page_list_size = page_list_size
        self.page_num = self.get_page_num()
    
    
    def get_pre_page_no(self, cur_page_no):
        """
        获取前一页的号码,第1页的前一页也是1
        """
        return max(cur_page_no-1, 1)
        
    
    def get_nex_page_no(self, cur_page_no):
        """
        获取下一页的号码,最后1页的下一页也是最后1页
        """
        return min(cur_page_no+1, self.page_num)
        
    
    def get_page_num(self):
        """
        根据obj的数量和每个page含有obj的数目,计算出有多少页面
        """
        page_num = self.count / self.page_size + 2
        if self.count % self.page_size == 0 and self.count > 0:
            page_num -= 1
        return page_num
    
    
    def get_objects_by_pageno(self, k):
        """
        根据页号k获取该页下的所有obj对象,返回列表[obj1,obj2,...]
        """
        return self.page_size * (int(k) - 1), min(self.page_size * int(k), self.count)
        
        
    def get_pages_list(self, cur_page):
        """
        根据页号cur_page获取该页下方的页号列表,返回[page_no1,page_no2,...]
        """
        if cur_page <= 6:
            return range(1, min(self.page_num, 11))
        else: 
            return range(cur_page-5, min(cur_page+5, self.page_num))

