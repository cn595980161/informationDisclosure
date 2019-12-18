package com.ricelink.fund.disclosure.service.impl;

import com.ricelink.fund.disclosure.service.BusinessService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class BusinessServiceImpl implements BusinessService {

    @Override
    public void crawlBase() {
        log.info("开始爬取基本信息");
        log.info("结束爬取基本信息");
    }

}
