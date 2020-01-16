package com.ricelink.fund.disclosure.web;

import com.ricelink.fund.disclosure.server.ProductWebSocket;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@RequestMapping("/")
public class IndexController {

    @RequestMapping("index")
    public String index() {
        return "main";
    }

    @ResponseBody
    @GetMapping("test")
    public String test(String userId, String message) throws Exception {
        if (userId == "" || userId == null) {
            return "发送用户id不能为空";
        }
        if (message == "" || message == null) {
            return "发送信息不能为空";
        }
        new ProductWebSocket().systemSendToUser(userId, message);
        return "发送成功！";
    }

    @RequestMapping(value = "/ws")
    public String ws() {
        return "ws";
    }

    @RequestMapping(value = "/ws1")
    public String ws1() {
        return "ws1";
    }

    @RequestMapping(value = "/test11")
    public String test() {
        return "test";
    }

    @RequestMapping(value = "/fund")
    public String fund() {
        return "fund_manager";
    }

    @RequestMapping(value = "/notice")
    public String notoce() {
        return "notice_manager";
    }

    @RequestMapping(value = "/paper")
    public String paper() {
        return "paper_manager";
    }

    @RequestMapping(value = "/rule")
    public String rule() {
        return "rule_manager";
    }

    @RequestMapping(value = "/report")
    public String report() {
        return "report_manager";
    }
}
