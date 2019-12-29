package com.ricelink.fund.disclosure.web;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/")
public class IndexController {

    @RequestMapping("index")
    public String index() {
        return "main";
    }
}
