from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://root:mysql@localhost/sql_test')

Session = sessionmaker(bind=engine)   #绑定引擎
session = Session()     #创建session对象


from sqlalchemy.orm import load_only
from sqlalchemy import func

#______________________________________
from models import Student,Teacher,Score,Grade,Course
# 1,查询student表中所有记录的sname和sclass
# sql: select sname,ssex from student
d1 = session.query(Student).options(load_only(Student.sname,Student.ssex)).all()
# for i in d1:
#     print(i)


# 2,查询教师所有的单位即不重复的depart列
# sql: select distinct(depart) from teacher
d2 = session.query(func.distinct(Teacher.depart)).all()
# print(d2)


#3，查询学生表的所有记录
# sql : select * from student;
d3 = session.query(Student).all()
print([i.sname for i in d3])    #只打印name

#4, 查询Score表中成绩在60到80之间的所有记录
# sql ：select * from score where degree between 60 and 80;
dt = session.execute("select * from score where degree between 60 and 80")  #使用原生sql
print([i.degree for i in dt])

d4 = session.query(Score.degree).filter(Score.degree.between(60,80)).all()
print([i.degree for i in d4])


# 5,查询Score表中成绩为85，86，88的记录：
# sql: select * from score where degree=85 or degree=86 or degrdd=88
# sql: select * from score where degree in (85,86,88)

d5 = session.query(Score).filter(or_(Score.degree==85,Score.degree==86,Score.degree==88)).all()
# print(d5)

d5 = session.query(Score).filter(Score.degree.in_([85,86,88])).all()
# print(d5)

# 6,查询学生表中95031班或性别为女的同学记录
# sql: select * from student where sclass ='95031' or ssex='女';
d6 = session.query(Student).filter(or_(Student.sclass=='95031',Student.ssex=='女')).all()
# print(d6)

# 7,以sclass 降序查询学生score表的所有记录
# sql: select * from score order by sclass desc;
d7 = session.query(Student).order_by(Student.sclass.desc()).all()
# print(d7)

# 8,以cno升序，degree降序查询score表的所有记录
# sql: select * from score order by sno,degree desc;
d8 = session.query(Score).order_by(Score.sno,Score.degree.desc()).all()
for i in d8:
    print(i)
print(d8)

# 9.查询95031班的学生人数
# sql: select count(sno) from student where sclass = '95031';
d9 = session.query(func.count(Student.sno).label('number')).filter(Student.sclass == '95031').all()
print(d9[0].number)
d9 = session.query(Student).filter(Student.sclass == '95031').count()  #直接使用了count
print(d9)

# 10 查询score表中的最高分的学生学号和课程号
# sql : select sno, cno from score order by degree desc limit 1;
d10 = session.query(Score).order_by(Score.degree.desc()).first()
# print(d10.sno,d10.cno)

# 11, 查询每门课的平均成绩
# sql: select cno,avg(degree) from score group by cno;
d11 = session.query(Score.cno,func.avg(Score.degree)).group_by(Score.cno).all()
# print(d11)
d111 = session.query(Course.cname,Score.cno,func.avg(Score.degree)).filter(Course.cno == Score.cno).group_by(Score.cno)
# print(d111)

# 12 查询Score表中至少有5名学生选修的并以3开头的课程的平均分数。
# sql: select avg(degree) from score where cno like '3%' group by cno having count(cno)>4;
d12 = session.query(Score.cno,func.avg(Score.degree)).filter(Score.cno.like('3%')).group_by(Score.cno).having(func.count(Score.cno)>4).all()
# print(d12)


#13 查询分数大于70，小于90的Sno列
# sql : select sno,degree from Score where degree between 70 and 90;
d13 = session.query(Score.sno,Score.degree).filter(Score.degree.between(70,90)).all()
# print(d13)

# 14、查询所有学生的Sname、Cno和Degree列。
# sql : select sname,cno,degree from Student left join Score on Score.sno=Student.sno;
d14 = session.query(Student.sname,Score.cno,Score.degree).join(Score,Score.sno==Student.sno).all()
# for i in d14:
#     print(i)


# 15、查询所有学生的Sno、Cname和Degree列。
# 16、查询所有学生的Sname、Cname和Degree列


# 17、 查询“95033”班学生的平均。
# sql: select avg(degree) from student left join score on student.sno = score.sno and student.sclass='95033';
d17 = session.query(func.avg(Score.degree)).join(Student,Student.sno==Score.sno).filter(Student.sclass=='95033').all()
# print(d17)


# 18、 假设使用如下命令建立了一个grade表：

# create table grade(low  int(3),upp  int(3),rank  char(1))
# insert into grade values(90,100,’A’)
# insert into grade values(80,89,’B’)
# insert into grade values(70,79,’C’)
# insert into grade values(60,69,’D’)
# insert into grade values(0,59,’E’)

# 现查询所有同学的Sno、Cno和rank列。

# sql: select sno,cno,degree,rank from Score inner join Grade on Score.degree between Grade.low and Grade.upp;
d18 = session.query(Score.sno,Score.cno,Score.degree,Grade.rank).join(Grade,Score.degree.between(Grade.low,Grade.upp)).all()
# for i in d18:
#     print(i)


# 19、  查询选修“3-105”课程的成绩高于“109”号同学成绩的所有同学的记录。
# select * from student inner join score on student.sno=score.sno where score.cno='3-105' and score.degree > (select degree from score where sno='109' and cno='3-105');

d19 = session.query(Student.sno,Student.sname,Student.sbirthday,Student.sclass).join(Score,Student.sno==Score.sno).\
    filter(and_(Score.cno=='3-105',Score.degree>(session.query(Score.degree).filter(and_(Score.sno=='109',Score.cno=='3-105'))))).all()
for i in d19:
    print(i.sno,i.sname)


# 20、查询score中选学多门课程的同学中分数为非最高分成绩的记录。
# sql: select * from score a inner join (
#     select sno,max(degree)as d from score group by sno HAVING count(sno) >1) as b on a.sno = b.sno where a.degree < b.d

sub_data = session.query(Score.sno,func.max(Score.degree).label('max')).group_by(Score.sno).having(func.count(Score.sno)>1).subquery()
d20 = session.query(Score.sno,Score.cno,Score.degree,sub_data.c.max).join(sub_data,Score.sno == sub_data.c.sno).filter(Score.degree < sub_data.c.max).all()
for i in d20:
    print(i)


# 21、查询选修“3-105”课程的成绩高于“109”号同学成绩的所有同学的记录。
# sql：select * from score as a inner join (select degree,cno from score where sno = '109' and cno = '3-105')as b on a.cno=b.cno where a.degree > b.degree;
from sqlalchemy import and_
#使用子查询的方式，运用subquery()
subquery = session.query(Score.cno,Score.degree).filter(and_(Score.sno == '109',Score.cno =='3-105')).subquery()
d21 = session.query(Score.sno,Score.cno,Score.degree,subquery.c.degree).join(subquery,Score.cno == subquery.c.cno).filter(Score.degree>subquery.c.degree).all()
for i in d21:
    print(i)
print("_"*30)

# sql : select * from student inner join score on student.sno = score.sno and score.cno = '3-105' having score.degree > (select degree from score where sno = '109' and cno = '3-105')
subquery = session.query(Score.cno,Score.degree).filter(and_(Score.sno=='109',Score.cno == '3-105')).first()
# print(subquery.c.degree)
print(subquery.degree)
d21 = session.query(Student.sno,Student.sname,Student.sclass,Score.cno,Score.degree).join(Score,and_(Student.sno == Score.sno,Score.cno=='3-105')).having(Score.degree>subquery.degree).all()
for i in d21:
    print(i)


# 22, 查询和学号为107的同学同年出生的所有学生的sno,sname,和sbirthday
# sql: select * from student where year(sbirthday) = (select year(sbirthday) from student where sno='107');

subquery = session.query(func.year(Student.sbirthday).label('bir')).filter(Student.sno=='107').subquery()
d22 = session.query(Student.sno,Student.sname,Student.sbirthday).filter(func.year(Student.sbirthday)==subquery.c.bir).all()
print(d22)


# 23、查询“张旭“教师任课的学生成绩。
# sql: select tno from Teacher where tname = '张旭';
#     select * from student inner join score on student.sno=score.sno inner join course on score.cno=course.cno inner join teacher on course.tno=teacher.tno having teacher.tname='张旭';
d23 = session.query(Student.sno,Student.sname,Teacher.tno,Score.degree).join(Score,Student.sno==Score.sno).join(Course,Score.cno==Course.cno).join(Teacher,Course.tno==Teacher.tno).filter(Teacher.tname=='张旭').all()
for i in d23:
    print(i)

# 24、查询选修某课程的同学人数多于5人的教师姓名。
# sql: select * from score group by cno HAVING count(cno) >5;
d24 = session.query(Teacher.tno,Teacher.tname).join(Course,Course.tno==Teacher.tno).join(Score,Score.cno==Course.cno).group_by(Score.cno).having(func.count(Score.cno)>5).all()
for i in d24:
    print(i)

# 25、查询95033班和95031班全体学生的记录。
# sql: select * from student where sclass='95033' or sclass='95031';
d25 = session.query(Student.sno,Student.sname).filter(or_(Student.sclass=='95033',Student.sclass=='95031')).all()
for i in d25:
    print(i)

# 26、  查询存在有85分以上成绩的课程Cno.
# sql： select DISTINCT(cno) from Score where degree>85;
d26 = session.query(func.distinct(Score.cno)).filter(Score.degree>85).all()
for i in d26:
    print(i)

# 27、查询出“计算机系“教师所教课程的成绩表。
# sql: select * from score inner join course on score.cno=course.cno where course.cname='计算机导论';
d27 = session.query(Score.sno,Score.cno,Score.degree).join(Course,Course.cno==Score.cno).filter(Course.cname=='计算机导论').all()
for i in d27:
    print(i)

# 28、查询“计算机系”与“电子工程系“不同职称的教师的Tname和Prof。
# sql: select * from teacher inner join course on teacher.tno=course.tno where course.cname='计算机导论' or course.cname='数字电路';
d28 = session.query(Teacher.tname,Teacher.prof).join(Course,Teacher.tno==Course.tno).filter(or_(Course.cname=='计算机导论',Course.cname=='数字电路')).all()
for i in d28:
    print(i)

# 29、查询选修编号为“3-105“课程且成绩至少高于选修编号为“3-245”的同学的Cno、Sno和Degree,并按Degree从高到低次序排序。
# sql: select a.cno,a.sno,a.degree from score a inner join score b on a.sno=b.sno where a.cno='3-105' and b.cno='3-245' and a.degree>b.degree ORDER BY a.degree;
subquery = session.query(Score.sno, Score.cno, Score.degree).subquery()
d29 = session.query(Score.cno, Score.sno, Score.degree).join(subquery, Score.sno == subquery.c.sno).filter(
    and_(Score.cno == '3-105', subquery.c.cno == '3-245')).order_by(Score.degree.desc()).all()
for i in d29:
    print(i)

# 30、查询选修编号为“3-105”且成绩高于选修编号为“3-245”课程的同学的Cno、Sno和Degree.
# 31、 查询所有教师和同学的name、sex和birthday.
# sql: select sname as n,ssex as s,sbirthday as b from student union selecct tname as n,tsex as s,tbirthday as b from teacher;
s1 = session.query(Student.sname.label('n'),Student.ssex.label('s'),Student.sbirthday.label('b'))
s2 = session.query(Teacher.tname.label('n'),Teacher.tsex.label('s'),Teacher.tbirthday.label('b'))
d31 = s1.union(s2).all()
for i in d31:
    print(i)

# 32、查询所有“女”教师和“女”同学的name、sex和birthday.
# sql: select tname as name,tsex as sex,tbirthday as b from teacher where tsex='女' union select sname as name,ssex as sex,sbirthday as b from student where ssex='女';
s1 = session.query(Teacher.tname.label('name'),Teacher.tsex.label('sex'),Teacher.tbirthday.label('b')).filter(Teacher.tsex=='女')
s2 = session.query(Student.sname.label('name'),Student.ssex.label('sex'),Student.sbirthday.label('b')).filter(Student.ssex=='女')
d32 = s1.union(s2).all()
for i in d32:
    print(i)


# 33、 查询成绩比该课程平均成绩低的同学的成绩表。
# sql: select sno,score.cno,degree from score inner join (select cno,avg(degree) as dg from score group by cno) as b on score.cno=b.cno where score.degree>b.dg;
subquery = session.query(Score.cno.label('c'),func.avg(Score.degree).label('avg_deg')).order_by(Score.cno).subquery()
d33 = session.query(Score.sno,Score.cno,Score.degree).join(subquery,Score.cno==subquery.c.c).filter(Score.degree>subquery.c.avg_deg).all()
for i in d33:
    print(i)

# 34、 查询所有任课教师的Tname和Depart.
# sql: select tname,depart from teacher;
d34 = session.query(Teacher.tname,Teacher.depart).all()
for i in d34:
    print(i)

# 子查询的使用————
# 35 、 查询所有未讲课的教师的Tname和Depart.
# sql :SELECT tname,depart from teacher where tname not in (select DISTINCT(tname) from teacher,course,score where teacher.tno=course.tno and course.cno=score.cno)
# subquery = session.query(func.distinct(Teacher.tname).label('n')).join(Course,Teacher.tno==Course.tno).join(Score,Course.cno==Score.cno).subquery()
# d35 = session.query(Teacher.tname,Teacher.depart).filter(Teacher.tname.in_(subquery.c.n)).all()

d35 = session.query(Teacher.tname,Teacher.depart).filter(~Teacher.tname.in_(session.query(func.distinct(Teacher.tname).label('n')).join(Course,Teacher.tno==Course.tno).join(Score,Course.cno==Score.cno))).all()
for i in d35:
    print(i)

# 36、查询至少有2名男生的班号。
# sql: select sclass from student where ssex='男' group by sclass having count(sno)>1;
d36 = session.query(Student.sclass).filter(Student.ssex=='男').group_by(Student.sclass).having(func.count(Student.sno)>1).all()
for i in d36:
    print(i)


# 37、查询Student表中不姓“王”的同学记录。
# sql: select * from student where sname not like '王%';
d37 = session.query(Student.sno,Student.sname,Student.ssex,Student.sclass).filter(~Student.sname.like('王%')).all()
for i in d37:
    print(i)

# 38、查询Student表中每个学生的姓名和年龄。
# sql: select sname,year(curdate())-year(sbirthday) from student;
d38 = session.query(Student.sname,func.year(func.current_date())-func.year(Student.sbirthday)).all()
for i in d38:
    print(i)

# 39、查询Student表中最大和最小的Sbirthday日期值。
# sql: select max(day(sbirthday)),min(day(sbirthday)) from student;
d39 = session.query(func.max(func.day(Student.sbirthday)),func.min(func.day(Student.sbirthday))).all()
for i in d39:
    print(i)


# 40、以班号和年龄从大到小的顺序查询Student表中的全部记录。
# sql: select * from student order by sclass desc,year(curdate())-year(sbirthday) desc,month(sbirthday);
d40 = session.query(Student.sno,Student.sname,Student.sbirthday).order_by(Student.sclass.desc(),func.current_date()-func.year(Student.sbirthday).desc()).all()
for i in d40:
    print(i)

# 41、查询“男”教师及其所上的课程。
# sql: select * from course inner join teacher on course.tno=teacher.tno where teacher.tsex='男';
d41 = session.query(Teacher.tname,Teacher.tsex,Course.cname).join(Course,Teacher.tno==Course.tno).filter(Teacher.tsex=='男').all()
for i in d41:
    print(i)

# 42、查询最高分同学的Sno、Cno和Degree列。
# sql: select * from score where degree >= (select max(degree) from score);
d42 = session.query(Score.sno,Score.cno,Score.degree).filter(Score.degree>=(session.query(func.max(Score.degree)))).all()
for i in d42:
    print(i)

# 43、查询和“李军”同性别的所有同学的Sname.
# sql: select sname from student where ssex = (select ssex from student where sname='李军')
d43 = session.query(Student.sname).filter(Student.ssex==(session.query(Student.ssex).filter(Student.sname=='李军'))).all()
for i in d43:
    print(i)

# 44、查询和“李军”同性别并同班的同学Sname.
# sql: select a.sname from student as a inner join (select ssex,sclass from student where sname='李军')as b on a.ssex=b.ssex and a.sclass=b.sclass;
subquery = session.query(Student.ssex,Student.sclass).filter(Student.sname=='李军').subquery()
d44 = session.query(Student.sname).join(subquery,and_(Student.ssex==subquery.c.ssex,Student.sclass==subquery.c.sclass)).all()
for i in d44:
    print(i)

# 45、查询所有选修“计算机导论”课程的“男”同学的成绩表
# sql: select * from score where cno = (select cno from course where cname='计算机导论') and sno in (select sno from student where ssex='男')
d45 = session.query(Score.sno,Score.cno,Score.degree).filter(Score.cno==(session.query(Course.cno).filter(Course.cname=='计算机导论')),Score.sno.in_(session.query(Student.sno).filter(Student.ssex=='男'))).all()
for i in d45:
    print(i)




# 1,不使用.all() 或.first() 等查询时，session对象就是一个sql语句。
# 2, union 的使用,将两张表连接