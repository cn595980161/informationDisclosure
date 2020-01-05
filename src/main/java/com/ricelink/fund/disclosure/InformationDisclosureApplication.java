package com.ricelink.fund.disclosure;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@EnableAsync
@SpringBootApplication
public class InformationDisclosureApplication {

	public static void main(String[] args) {
		SpringApplication.run(InformationDisclosureApplication.class, args);
	}

}
