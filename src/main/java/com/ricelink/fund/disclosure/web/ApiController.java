package com.ricelink.fund.disclosure.web;

import com.ricelink.fund.disclosure.core.ResponseGenerate;
import com.ricelink.fund.disclosure.core.ResponseMsg;
import com.ricelink.fund.disclosure.model.Fund;
import com.ricelink.fund.disclosure.service.BusinessService;
import com.ricelink.fund.disclosure.util.ExcelUtils;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.List;

@Slf4j
@Controller
@RequestMapping("api")
public class ApiController {

    @Value("${setting.project.path}")
    private String projectPath;

    @Autowired
    BusinessService businessService;

    /**
     * 上传文件
     *
     * @param file
     */
    @ResponseBody
    @RequestMapping(value = "/upload", method = RequestMethod.POST)
    public ResponseMsg upload(@RequestParam("file") MultipartFile file) throws IOException {

        long start = System.currentTimeMillis();
        List<Fund> fundList = ExcelUtils.importExcel(file, Fund.class);
        log.debug(fundList.toString());
        log.debug("导入excel所花时间：" + (System.currentTimeMillis() - start));

        //复制文件
        FileUtils.copyInputStreamToFile(file.getInputStream(), new File(projectPath, "基金清单.xlsx"));

        return ResponseGenerate.success("操作成功!", fundList);
    }

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
     * 查询基金清单
     *
     * @return
     * @throws IOException
     */
    @ResponseBody
    @RequestMapping(value = "/queryFundList", method = RequestMethod.GET)
    public ResponseMsg queryFundList() throws IOException {
        List<Fund> fundList = ExcelUtils.importExcel(projectPath + File.separator + "基金清单.xlsx", 1, 1, Fund.class);
        log.debug(fundList.toString());
        return ResponseGenerate.success("成功!", fundList);
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
    public ResponseMsg cancelUpdateNotice(@RequestParam String processId) {
        businessService.cancelUpdateNotice(processId);
        return ResponseGenerate.success("操作成功!");
    }

    /**
     * 下载公告
     *
     * @param filename
     * @return
     * @throws IOException
     */
    @ResponseBody
    @RequestMapping(value = "downloadNotice")
    public ResponseEntity<byte[]> download(@RequestParam("fileName") String filename) throws IOException {

        File file = new File("E:\\info_disc_flask\\全量公告.xls");
        HttpHeaders headers = new HttpHeaders();
        headers.setContentDispositionFormData("attachment", new String(file.getName().getBytes("utf-8"), "ISO8859-1"));
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        return new ResponseEntity<>(FileUtils.readFileToByteArray(file), headers, HttpStatus.OK);
    }

}
