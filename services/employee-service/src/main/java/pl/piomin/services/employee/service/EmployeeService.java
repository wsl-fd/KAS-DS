package pl.piomin.services.employee.service;

import pl.piomin.services.employee.model.Employee;

public interface EmployeeService {

    boolean add(Employee employee);

    Employee findById(int id);

    boolean deleteById(int id);

    Iterable<Employee> findAll();

    // void xxe();
}