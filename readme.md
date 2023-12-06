## Architecture
- **gateway-service** - a module that Spring Cloud Netflix Zuul for running Spring Boot application that acts as a proxy/gateway in our architecture.
- **employee-service** - a tomcat service containing the first of our sample microservices that allows to perform CRUD operation on Mongo repository of employees
- **department-service** - a module containing the second of our sample microservices that allows to perform CRUD operation on Mongo repository of departments. It communicates with employee-service. 
- **organization-service** - a module containing the third of our sample microservices that allows to perform CRUD operation on Mongo repository of organizations. It communicates with both employee-service and department-service.
- **redis-service** - a redis db for caching.
- **mysql-service** - a MySQL db.

Application CVE exploit:
1. CVE-2022-22965 Spring Framework RCE via Data Binding on JDK 9+
2. CVE-2022-22947 Spring Cloud Gateway Actuator API SpEL Code Injection 
3. CVE-2022-0543 Redis Lua Sandbox Escape and Remote Code Execution 
4. CVE-2020-1938 Aapache Tomcat AJP Arbitrary File Read / Include Vulnerability
5. CVE-2012-2122 Mysql Authorization Bypass

Anormal access:
1. Direct Redis access
2. Direct MySQL access

Misconfig exploit:
1. Mounted Docker.sock Abuse
2. Kubeconfig Abuse
3. Host Mount Abuse


You can easily deploy all applications using `skaffold dev` command.
