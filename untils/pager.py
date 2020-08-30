class Pagination(object):
    def __init__(self,totalCount,currentPage,perPageItemNum=5,maxPageNum=7):
        # 数据总个数
        self.total_count = totalCount
        # 当前页
        try:
            v = int(currentPage)
            if v <= 0:
               v = 1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        # 每页显示的数据行数
        self.per_page_item_num = perPageItemNum
        # 最多显示的页数
        self.max_page_num = maxPageNum

    def start(self):#一页的开始数据
        return (self.current_page-1) * self.per_page_item_num

    def end(self):  #一页的结束数据
        return self.current_page * self.per_page_item_num

    @property #总页数  @property 可以去掉括号变成方法调用
    def num_pages(self):
        """
        总页数
        :return:
        """
        # 666
        # 10
        #divmod 得出除后的 整数a 和 余数b
        a,b = divmod(self.total_count,self.per_page_item_num)
        if b == 0:
            return a
        return a+1  #有余数就多返回一页

    #返回页码
    def pager_num_range(self):
        # 当前页            self.current_page
        # 最多显示的页数    self.max_page_num
        # 总页数           self.num_pages

        if self.num_pages < self.max_page_num:  #总页数<最多显示页数时
            return range(1,self.num_pages+1)
        # 总页数特别多 5
        part = int(self.max_page_num/2)
        if self.current_page <= part:
            return range(1,self.max_page_num+1)
        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages-self.max_page_num+1,self.num_pages+1)
        return range(self.current_page-part,self.current_page+part+1)

    #后端生产页码
    def page_str(self,base_url):
        page_list=[] #下面的 页码条

        #首页
        first_page="<li><a href='%s?p=1'>首页</a></li>" %(base_url,)
        page_list.append(first_page)
        #上一页
        if self.current_page==1:
            page_pre="<li><a href='javascript:void(0)'>上一页</a></li>"
        else:
            page_pre="<li><a href='%s?p=%s'>上一页</a></li>" %(base_url,self.current_page-1,)
        page_list.append(page_pre)

        #页码
        for i in self.pager_num_range():
            if i==self.current_page:
                temp="<li class='active'><a href='%s?p=%s'>%s</a></li>" %(base_url,i,i)
            else:
                temp="<li><a href='%s?p=%s'>%s</a></li>" %(base_url,i,i)
            page_list.append(temp)

        #下一页
        if self.current_page == self.num_pages:
            page_next = "<li><a href='javascript:void(0)'>下一页</a></li>"
        else:
            page_next = "<li><a href='%s?p=%s'>下一页</a></li>" % (base_url,self.current_page + 1,)
        page_list.append(page_next)

        #尾页
        last_page="<li><a href='%s?p=%s'>尾页</a>" %(base_url,self.num_pages)
        page_list.append(last_page)
        return ''.join(page_list)