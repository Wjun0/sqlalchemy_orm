from sqlalchemy import Integer,String,Column,DateTime  #导入数据类型
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    sno = Column(Integer, primary_key=True, doc='学号')
    sname = Column(String, doc='姓名')
    ssex = Column(String, doc='性别')
    sbirthday = Column(DateTime, doc='生日')
    sclass = Column(String, doc='班级')

    def __repr__(self):  # 将对象格式化输出
        return '%s (sno=%r,sname=%r,ssex=%r,sbirthday=%r,sclass=%r)' % (
            self.__class__.__name__, self.sno, self.sname, self.ssex, self.sbirthday, self.sclass)


class Teacher(Base):
    __tablename__ = 'teacher'
    tno = Column(String, primary_key=True, doc='教师号')
    tname = Column(String)
    tsex = Column(String)
    tbirthday = Column(DateTime)
    prof = Column(String)
    depart = Column(String)

    def __repr__(self):
        return '%s (tno=%r,tname=%r,tsex=%r,tbirthday=%r,prot=%r,depart=%r)' % (
            self.__class__.__name__, self.tname, self.tname, self.tsex, self.tbirthday, self.prof, self.depart
        )


class Score(Base):
    __tablename__ = 'score'
    sno = Column(String, primary_key=True)
    cno = Column(String)
    degree = Column(Integer)

    def __repr__(self):
        return '%s (sno=%r,cno=%r,degree=%r)' % (
            self.__class__.__name__, self.sno, self.cno, self.degree
        )


class Course(Base):
    __tablename__ = 'course'
    cno = Column(String, primary_key=True)
    cname = Column(String)
    tno = Column(String)

    def __repr__(self):
        return '%s (cno=%r,sname=%r,tno=%r)' % (
            self.__class__.__name__, self.cno, self.sname, self.tno
        )


class Grade(Base):
    __tablename__ = 'grade'
    low = Column(Integer)
    upp = Column(Integer)
    rank = Column(String, primary_key=True)