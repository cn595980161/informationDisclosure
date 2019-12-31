from abc import ABCMeta, abstractmethod


# 接口类:
class BaseCrawl(metaclass=ABCMeta):

    @abstractmethod
    def crawl_info(self):
        """
        子类继承父类必须重写crawl_info方法
        :return:
        """
        raise NotImplementedError("crawl_info() 方法是必须的")

    @abstractmethod
    def crawl_year_report(self):
        """
        子类继承父类必须重写crawl_year_report方法
        :return:
        """
        raise NotImplementedError("crawl_year_report() 方法是必须的")
