package com.ricelink.fund.disclosure.service;

import com.ricelink.fund.disclosure.core.ResponseMsg;

public interface BusinessService {

    /**
     * 爬取基本信息
     */
    ResponseMsg crawlBase(String userId);

    /**
     * 取消爬取基本信息
     * @param processId
     */
    void cancelUpdateNotice(String processId);
}
