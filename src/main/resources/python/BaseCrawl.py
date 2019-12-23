class BaseCrawl(object):

    def crawl_history(self):
        """
        子类继承父类必须重写crawl_history方法
        :return:
        """
        raise NotImplementedError("crawl_history() 方法是必须的")

    def crawl_year_report(self):
        """
        子类继承父类必须重写crawl_year_report方法
        :return:
        """
        raise NotImplementedError("crawl_year_report() 方法是必须的")
