package com.ricelink.fund.disclosure.model;

import cn.afterturn.easypoi.excel.annotation.Excel;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;

@Data
@EqualsAndHashCode(callSuper = false)
public class Fund implements Serializable {

    @Excel(name = "基金编号", orderNum = "0", width = 15)
    private String fundCode;

    @Excel(name = "基金名称", orderNum = "1", width = 15)
    private String fundName;
}
