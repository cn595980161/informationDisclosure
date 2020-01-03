package com.ricelink.fund.disclosure.web;

import com.ricelink.fund.disclosure.model.Fund;
import com.ricelink.fund.disclosure.server.ProductWebSocket;
import com.ricelink.fund.disclosure.util.ExcelUtils;
import com.ricelink.fund.disclosure.util.ExecuteCmdUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import java.io.IOException;
import java.util.List;

@Slf4j
@Controller
@RequestMapping("api")
public class ApiController {

    @Resource
    private ProductWebSocket productWebSocket;

    /**
     * 导入
     *
     * @param file
     */
    @RequestMapping(value = "/import", method = RequestMethod.POST)
    public Object importExcel(@RequestParam("file") MultipartFile file) throws IOException {
        long start = System.currentTimeMillis();
        List<Fund> personVoList = ExcelUtils.importExcel(file, Fund.class);
        log.debug(personVoList.toString());
        log.debug("导入excel所花时间：" + (System.currentTimeMillis() - start));
        return personVoList;
    }

    @GetMapping("test")
    @ResponseBody
    public Object test(@RequestParam String userId) {
        ExecuteCmdUtil.execute(msg -> {
            System.out.println(msg);
            productWebSocket.systemSendToUser(userId, msg);
        }, "python3", "E:/项目/informationDisclosure/src/main/resources/python/cjhxCrawl.py");
        return "ojbk";
    }

}
