package com.ricelink.fund.disclosure.core;

public class ResponseGenerate {

    /**
     * 成功
     *
     * @param message
     */
    public static ResponseMsg success(String message) {
        return new ResponseMsg(ResponseMsg.SUCCESS, message, null);
    }

    /**
     * 成功
     *
     * @param message
     */
    public static ResponseMsg success(String message, Object data) {
        return new ResponseMsg(ResponseMsg.SUCCESS, message, data);
    }

    /**
     * 失败
     *
     * @param message
     */
    public static ResponseMsg fail(String message) {
        return new ResponseMsg(ResponseMsg.FAILED, message, null);
    }
}
