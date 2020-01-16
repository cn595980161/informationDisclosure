package com.ricelink.fund.disclosure.model;

import cn.afterturn.easypoi.excel.annotation.Excel;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;

@Data
@EqualsAndHashCode(callSuper = false)
public class Fund implements Serializable {

    @Excel(name = "产品代码", orderNum = "0", width = 15)
    private String fundCode;

    @Excel(name = "账套全称", orderNum = "1", width = 15)
    private String fundName;
}
