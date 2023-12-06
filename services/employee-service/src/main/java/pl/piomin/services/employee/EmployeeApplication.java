package pl.piomin.services.employee;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
// import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.boot.builder.SpringApplicationBuilder;


@SpringBootApplication
@EnableDiscoveryClient
@EnableCaching

@MapperScan("pl.piomin.services.employee.repository")
// @EnableMongoRepositories
public class EmployeeApplication extends SpringBootServletInitializer{

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
	   return application.sources(EmployeeApplication.class);
	}

    public static void main(String[] args) {
        SpringApplication.run(EmployeeApplication.class, args);
    }

}
