create table employees
(
    id          int(4)                     not null
        primary key AUTO_INCREMENT,
    name        varchar(64)                not null,
    organizationId        varchar(128)     not null,
    departmentId         varchar(128)      null,
    position             varchar(128)      null ,
    age         int(2)      null ,
    create_time timestamp  default CURRENT_TIMESTAMP null,
    status      tinyint(1) default 1      not null
);