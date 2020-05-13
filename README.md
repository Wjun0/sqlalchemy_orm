# sqlalchemy_orm
sqlalchemy 查询语句</br>
1, 中文文档：https://www.osgeo.cn/sqlalchemy/orm <br>
2, 英文文档：https://docs.sqlalchemy.org/en/13/orm <br>
3,该示例使用sqlalchemy1.3.12版本,主外键关系连接查询看文档<br>

**注意点**<br>
1, 不使用.all() 或.first() 等查询时，session对象就是一个sql语句。<br>
2, union 的使用,将两张表连接<br>
3, 表别名：select * from my_customer_table as customer <br>
customer = my_customer_table.alias('customer') <br>

4, 列别名 select user.name as username from user<br>
columns = [<br>
    customer,<br>
    user.c['name'].label('username')<br>
]<br>
