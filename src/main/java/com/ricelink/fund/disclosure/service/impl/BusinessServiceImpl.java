package com.ricelink.fund.disclosure.service.impl;

import com.ricelink.fund.disclosure.server.ProductWebSocket;
import com.ricelink.fund.disclosure.service.BusinessService;
import com.ricelink.fund.disclosure.server.ExecuteCmdServer;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
@Slf4j
public class BusinessServiceImpl implements BusinessService {

    @Resource
    private ProductWebSocket productWebSocket;

    @Resource
    private ExecuteCmdServer executeCmdServer;

    @Override
    public String crawlBase(String userId) {
        log.info("开始爬取基本信息");
        String processId = executeCmdServer.createProcess("python", "D:\\项目\\informationDisclosure\\src\\main\\resources\\python\\cjhxCrawl.py");
        executeCmdServer.asyncExecute(msg -> {
            System.out.println(msg);
            productWebSocket.systemSendToUser(userId, msg);
        }, processId);

        System.out.println(processId);
        log.info("结束爬取基本信息");
        return processId;
    }

    @Override
    public void cancelUpdateNotice(String processId) {
        executeCmdServer.cancelExecute(processId);
    }

}
