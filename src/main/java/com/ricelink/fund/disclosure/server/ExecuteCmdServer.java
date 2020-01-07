package com.ricelink.fund.disclosure.server;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Component
//@PropertySource(value = "classpath:application.properties", encoding = "UTF-8")
public class ExecuteCmdServer {

    @Value("${setting.python.path}")
    private String pythonDirectory;

    //process对象map
    private static ConcurrentHashMap<String, Process> processSet = new ConcurrentHashMap();

    /**
     * 执行命令
     *
     * @param command
     * @param handleConsole
     * @return
     */
    public String execute(HandleConsole handleConsole, String... command) {
        ProcessBuilder pb = new ProcessBuilder(command);

        pb.redirectErrorStream(true);

        try {
            //启动进程
            Process process = pb.start();

            //获取输入流
            InputStream inputStream = process.getInputStream();
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
            process.destroy();
            return outputString.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }


    /**
     * 执行命令
     *
     * @param command
     * @return pid
     */
    public String createProcess(String... command) throws IOException {
        ProcessBuilder pb = new ProcessBuilder(command);
        //cmd执行路径
        pb.directory(new File(pythonDirectory));
        //ErrorStreams合并
        pb.redirectErrorStream(true);
        Process process = pb.start();
        String processId = UUID.randomUUID().toString();
        processSet.put(processId, process);
        return processId;
    }


    /**
     * 执行命令
     *
     * @param handleConsole
     * @param processId
     * @return
     */
    @Async
    public String asyncExecute(HandleConsole handleConsole, String processId) {
        try {
            Process process = processSet.get(processId);
            //获取输入流
            InputStream inputStream = process.getInputStream();
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
            process.destroy();
            return outputString.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 取消执行命令
     *
     * @param processId
     * @return
     */
    public void cancelExecute(String processId) {
        Process process = processSet.get(processId);
        process.destroyForcibly();
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

//    public static void main(String[] args) {
//        execute(msg -> {
//            System.out.println(msg);
//        }, "python3", "E:/项目/informationDisclosure/src/main/resources/python/cjhxCrawl.py");
//    }
}
