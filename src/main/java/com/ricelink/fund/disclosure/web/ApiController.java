package com.ricelink.fund.disclosure.web;

import com.ricelink.fund.disclosure.model.Fund;
import com.ricelink.fund.disclosure.util.ExcelUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@Slf4j
@RestController
@RequestMapping("excel")
public class ApiController {

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
}
