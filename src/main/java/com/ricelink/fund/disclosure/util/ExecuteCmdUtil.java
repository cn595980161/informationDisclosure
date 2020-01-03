package com.ricelink.fund.disclosure.util;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class ExecuteCmdUtil {

    /**
     * 执行命令
     *
     * @param command
     * @param handleConsole
     * @return
     */
    public static String execute(HandleConsole handleConsole, String... command) {
        //"python3", "E:/项目/informationDisclosure/src/main/resources/python/cjhxCrawl.py"
        ProcessBuilder pb = new ProcessBuilder(command);

//        //redirectErrorStream 属性默认值为false，意思是子进程的标准输出和错误输出被发送给两个独立的流，这些流可以通过 Process.getInputStream() 和 Process.getErrorStream() 方法来访问。
//        //如果将值设置为 true，标准错误将与标准输出合并。这使得关联错误消息和相应的输出变得更容易。在此情况下，合并的数据可从 Process.getInputStream() 返回的流读取，而从 Process.getErrorStream() 返回的流读取将直接到达文件尾。
        pb.redirectErrorStream(true);
//        pb.redirectOutput(Redirect.appendTo(log));

        try {
            //启动进程
            Process start = pb.start();
            //获取输入流
            InputStream inputStream = start.getInputStream();
            //转成字符输入流
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream, "gbk");
            int len;
            char[] c = new char[1024];
            StringBuffer outputString = new StringBuffer();
            //读取进程输入流中的内容
            while ((len = inputStreamReader.read(c)) != -1) {
                String s = new String(c, 0, len);
                outputString.append(s);
//                System.out.print(s);
                handleConsole.print(s);
            }
            inputStream.close();
            start.destroy();
            return outputString.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 处理接口
     */
    public interface HandleConsole {

        /**
         * 打印方法
         */
        void print(String msg);
    }

    public static void main(String[] args) {
        execute(msg -> {
            System.out.println(msg);
        }, "python3", "E:/项目/informationDisclosure/src/main/resources/python/cjhxCrawl.py");
    }
}
