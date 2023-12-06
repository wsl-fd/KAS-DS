package pl.piomin.services.employee.repository;

import java.util.List;

// import org.springframework.data.repository.CrudRepository;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Result;
import org.apache.ibatis.annotations.Results;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import pl.piomin.services.employee.model.Employee;

// @Repository
// @Mapper
public interface EmployeeRepository //extends CrudRepository<Employee, String> 
{

    // List<Employee> findByDepartmentId(String departmentId);

    // List<Employee> findByOrganizationId(String organizationId);


    @Select("SELECT * FROM employees")
	// @Results({
	// 	@Result(property = "userSex",  column = "user_sex", javaType = UserSexEnum.class),
	// 	@Result(property = "nickName", column = "nick_name")
	// })
	List<Employee> findAll();
	
	@Select("SELECT * FROM employees WHERE id = #{id}")
	Employee findById(int id);

	@Delete("DELETE FROM employees WHERE id = #{id}")
	int deleteById(int id);


	// @Update("UPDATE users SET userName=#{userName},nick_name=#{nickName} WHERE id =#{id}")
	// void update(User user);

	// @Delete("DELETE FROM users WHERE id =#{id}")
	// void delete(Long id);

	@Insert("INSERT INTO employees(name,organizationId,departmentId,position,age) VALUES(#{name}, #{organizationId}, #{departmentId}, #{position}, #{age})")
	int add(Employee employee);

	// @Select("SELECT * FROM employees WHERE name = xxe")
    // List<Employee> xxe();
}
