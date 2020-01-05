package com.ricelink.fund.disclosure.core;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.ToString;

import java.io.Serializable;

@Data
@AllArgsConstructor
@ToString
public class ResponseMsg<T> implements Serializable {

    private static final long serialVersionUID = 1L;

    public static final Integer SUCCESS = 200;

    public static final Integer FAILED = 0;

    private int code;

    private String msg;

    private T data;

}