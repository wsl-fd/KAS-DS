package pl.piomin.services.employee.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import pl.piomin.services.employee.model.Employee;
import pl.piomin.services.employee.repository.EmployeeRepository;
import pl.piomin.services.employee.service.EmployeeService;

@Service
@CacheConfig(cacheNames="employee")
public class EmployeeServiceImpl implements EmployeeService {

    @Autowired EmployeeRepository employeeRepository;

    @Override
    @CacheEvict(key = "'findAll'" )
    public boolean add(Employee employee) {
        return employeeRepository.add(employee) >0;
    }

    @Override
    @Cacheable(key="#id")
    public Employee findById(int id) {
        return employeeRepository.findById(id);
    }

    @Override
    // @Cacheable(key="#root.methodName")
    @Cacheable(key="'findAll'")
    public Iterable<Employee> findAll() {
        return employeeRepository.findAll();
    }
    
    @Override
    @CacheEvict(key = "'findAll'" )
    public boolean deleteById(int id){
        return employeeRepository.deleteById(id) > 0;
    }

    // @Override
    // public void xxe(){
    //     /* var l = employeeRepository.xxe();
    //     for (Employee employee : l) {
            
    //     } */
    // }
    
}
