package com.ricelink.fund.disclosure.service;

public interface BusinessService {

    /**
     * 爬取基本信息
     */
    String crawlBase(String userId);

    /**
     * 取消爬取基本信息
     * @param processId
     */
    void cancelUpdateNotice(String processId);
}
