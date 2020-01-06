package com.ricelink.fund.disclosure.service.impl;

import com.ricelink.fund.disclosure.core.ResponseGenerate;
import com.ricelink.fund.disclosure.core.ResponseMsg;
import com.ricelink.fund.disclosure.server.ExecuteCmdServer;
import com.ricelink.fund.disclosure.server.ProductWebSocket;
import com.ricelink.fund.disclosure.service.BusinessService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.io.IOException;

@Service
@Slf4j
@PropertySource(value = "classpath:application.properties", encoding = "UTF-8")
public class BusinessServiceImpl implements BusinessService {

    @Resource
    private ProductWebSocket productWebSocket;

    @Resource
    private ExecuteCmdServer executeCmdServer;

    @Override
    public ResponseMsg crawlBase(String userId) {
        log.info("开始爬取基本信息");
        try {
            String processId = executeCmdServer.createProcess("python", "cjhxCrawl.py");
            System.out.println(processId);
            executeCmdServer.asyncExecute(msg -> {
                System.out.println(msg);
                productWebSocket.systemSendToUser(userId, msg);
            }, processId);
            return ResponseGenerate.success("操作成功!", processId);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseGenerate.fail(e.getMessage());
        } finally {
            log.info("结束爬取基本信息");
        }
    }

    @Override
    public void cancelUpdateNotice(String processId) {
        executeCmdServer.cancelExecute(processId);
    }

}
