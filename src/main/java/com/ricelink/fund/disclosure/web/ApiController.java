package com.ricelink.fund.disclosure.web;

import com.ricelink.fund.disclosure.core.ResponseGenerate;
import com.ricelink.fund.disclosure.core.ResponseMsg;
import com.ricelink.fund.disclosure.model.Fund;
import com.ricelink.fund.disclosure.service.BusinessService;
import com.ricelink.fund.disclosure.util.ExcelUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@Slf4j
@Controller
@RequestMapping("api")
public class ApiController {

    @Autowired
    BusinessService businessService;

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

    /**
     * 更新公告信息
     *
     * @param userId
     * @return
     */
    @ResponseBody
    @GetMapping("updateNotice")
    public ResponseMsg updateNotice(@RequestParam String userId) {
        return businessService.crawlBase(userId);
    }

    /**
     * 取消更新公告信息
     *
     * @param processId
     * @return
     */
    @ResponseBody
    @GetMapping("cancelUpdateNotice")
    public Object cancelUpdateNotice(@RequestParam String processId) {
        businessService.cancelUpdateNotice(processId);
        return ResponseGenerate.success("操作成功!");
    }

}
