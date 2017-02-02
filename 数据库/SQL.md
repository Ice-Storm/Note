# SQL 语句概述
SQL 是用于访问和处理数据库的标准的计算机语言。

SQL 是一门 ANSI 的标准计算机语言，用来访问和操作数据库系统。SQL 语句用于取回和更新数据库中的数据。SQL 可与数据库程序协同工作，比如 MS Access、DB2、Informix、MS SQL Server、Oracle、Sybase 以及其他数据库系统。

不幸地是，存在着很多不同版本的 SQL 语言，但是为了与 ANSI 标准相兼容，它们必须以相似的方式共同地来支持一些主要的关键词（比如 SELECT、UPDATE、DELETE、INSERT、WHERE 等等）。

RDBMS 是 SQL 的基础，同样也是所有现代数据库系统的基础，比如 MS SQL Server, IBM DB2, Oracle, MySQL 以及 Microsoft Access。

RDBMS 中的数据存储在被称为表（tables）的数据库对象中。
表是相关的数据项的集合，它由列和行组成。

**注意**：以下语句大多以 MySQL 为主，其他数据库有少许不同。

## SQL 语法

### 创建
#### CREATE DATABASE
创建数据库。

```sql
CREATE DATABASE database_name
```
#### CREATE TABLE
```sql
CREATE TABLE 表名称
(
列名称1 数据类型,
列名称2 数据类型,
列名称3 数据类型,
....
)
```
#### CREATE INDEX
CREATE INDEX 语句用于在表中创建索引。
在不读取整个表的情况下，索引使数据库应用程序可以更快地查找数据。

```sql
CREATE INDEX index_name
ON table_name (column_name)
```

#### 数据类型
MySQL 有三种主要数据类型：文本、数字和日期/时间。


#### 约束(Constraints)
约束用于限制加入表的数据的类型
以在创建表时规定约束（通过 CREATE TABLE 语句），或者在表创建之后也可以（通过 ALTER TABLE 语句）。
我们将主要探讨以下几种约束：

- NOT NULL
- UNIQUE
- PRIMARY KEY
- FOREIGN KEY
- CHECK
- DEFAULT

##### NOT NULL
NOT NULL 约束强制列不接受 NULL 值。

```sql
CREATE TABLE Persons
(
Id_P int NOT NULL,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255)
)
```

##### UNIQUE
UNIQUE 约束唯一标识数据库表中的每条记录。

```sql
CREATE TABLE Persons
(
Id_P int NOT NULL,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255),
UNIQUE (Id_P)
)
```

##### PRIMARY KEY
PRIMARY KEY 约束唯一标识数据库表中的每条记录。
主键必须包含唯一的值。
主键列不能包含 NULL 值。
每个表都应该有一个主键，并且每个表只能有一个主键。

```sql
CREATE TABLE Persons
(
Id_P int NOT NULL,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255),
PRIMARY KEY (Id_P)
)
```
##### FOREIGN KEY
一个表中的 FOREIGN KEY 指向另一个表中的 PRIMARY KEY。

FOREIGN KEY 约束用于预防破坏表之间连接的动作。
FOREIGN KEY 约束也能防止非法数据插入外键列，因为它必须是它指向的那个表中的值之一。

```sql
CREATE TABLE Orders
(
Id_O int NOT NULL,
OrderNo int NOT NULL,
Id_P int,
PRIMARY KEY (Id_O),
FOREIGN KEY (Id_P) REFERENCES Persons(Id_P)
)
```

##### CHECK
CHECK 约束用于限制列中的值的范围。
如果对单个列定义 CHECK 约束，那么该列只允许特定的值。
如果对一个表定义 CHECK 约束，那么此约束会在特定的列中对值进行限制。

```sql
CREATE TABLE Persons
(
Id_P int NOT NULL,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255),
CHECK (Id_P>0)
)
```
##### DEFAULT
DEFAULT 约束用于向列中插入默认值。
如果没有规定其他的值，那么会将默认值添加到所有的新记录。

```sql
CREATE TABLE Persons
(
Id_P int NOT NULL,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255) DEFAULT 'Sandnes'
)
```

##### AUTO INCREMENT
我们通常希望在每次插入新记录时，自动地创建主键字段的值。
我们可以在表中创建一个 auto-increment 字段。

```sql
CREATE TABLE Persons
(
P_Id int NOT NULL AUTO_INCREMENT,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255),
PRIMARY KEY (P_Id)
)
```

要让 AUTO_INCREMENT 序列以其他的值起始，请使用下列 SQL 语法：
```sql
ALTER TABLE Persons AUTO_INCREMENT=100
```
### 修改
#### 添加
##### INSERT
INSERT INTO 语句用于向表格中插入新的行。

```sql
INSERT INTO 表名称 VALUES (值1, 值2,....)
INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
```
#### 更新
##### UPDATE
Update 语句用于修改表中的数据。

```sql
UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
```

#### 删除
##### DELETE
DELETE 语句用于删除表中的行。

```sql
DELETE FROM 表名称 WHERE 列名称 = 值
```

##### DROP
我们可以使用 DROP INDEX 命令删除表格中的索引。

```sql
ALTER TABLE table_name DROP INDEX index_name
```
DROP TABLE 语句用于删除表（表的结构、属性以及索引也会被删除

```sql
DROP TABLE 表名称
```
DROP DATABASE 语句用于删除数据库：

```sql
DROP DATABASE 数据库名称
```

##### TRUNCATE
如果我们仅仅需要除去表内的数据，但并不删除表本身，那么我们该如何做呢？
请使用 TRUNCATE TABLE 命令（仅仅删除表格中的数据）：

```sql
TRUNCATE TABLE 表名称
```
#### ALTER
ALTER TABLE 语句用于在已有的表中添加、修改或删除列。

如需在表中添加列，请使用下列语法:

```sql
ALTER TABLE table_name
ADD column_name datatype
```
要删除表中的列，请使用下列语法：

```sql
ALTER TABLE table_name 
DROP COLUMN column_name
```
### 查询
#### 过滤
##### SELECT
SELECT 语句用于从表中选取数据。
结果被存储在一个结果表中（称为结果集）。

```sql
SELECT 列名称 FROM 表名称
SELECT * FROM 表名称
```
##### SELECT DISTINCT 
在表中，可能会包含重复值。这并不成问题，不过，有时您也许希望仅仅列出不同（distinct）的值。
关键词 DISTINCT 用于返回唯一不同的值。

```sql
SELECT DISTINCT 列名称 FROM 表名称
```

##### WHERE
如需有条件地从表中选取数据，可将 WHERE 子句添加到 SELECT 语句。

```sql
如需有条件地从表中选取数据，可将 WHERE 子句添加到 SELECT 语句。
```
常用运算符：= <>, >, <, >=, <=, BETWEEN, LIKE

##### AND OR
AND 和 OR 可在 WHERE 子语句中把两个或多个条件结合起来

```sql
SELECT * FROM Persons WHERE FirstName='Thomas' AND LastName='Carter'
```

##### TOP
TOP 子句用于规定要返回的记录的数目(MySQL是 LIMIT)。

```sql
SELECT column_name(s)
FROM table_name
LIMIT number
```

##### LIKE
LIKE 操作符用于在 WHERE 子句中搜索列中的指定模式。

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name LIKE pattern
```
通配符有：

- %，替代一个或多个字符
- _，仅替代一个字符
- [charlist]，字符列中的任何单一字符
- [^charlist]或[!charlist]，不在字符列中的任何单一字符

##### IN
IN 操作符允许我们在 WHERE 子句中规定多个值。

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name IN (value1,value2,...)
```

##### BETWEEN
操作符 BETWEEN ... AND 会选取介于两个值之间的数据范围。这些值可以是数值、文本或者日期。

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name
BETWEEN value1 AND value2
```

#### 排序
##### ORDER BY
ORDER BY 语句用于根据指定的列对结果集进行排序。
ORDER BY 语句默认按照升序对记录进行排序。
如果您希望按照降序对记录进行排序，可以使用 DESC 关键字。

```sql
SELECT Company, OrderNumber FROM Orders ORDER BY Company
```

#### 合并
##### JOIN
有时为了得到完整的结果，我们需要从两个或更多的表中获取结果。我们就需要执行 join。

```sql
SELECT Persons.LastName, Persons.FirstName, Orders.OrderNo
FROM Persons, Orders
WHERE Persons.Id_P = Orders.Id_P 
```
##### INNER JOIN
在表中完全匹配时，INNER JOIN 关键字返回行。

```sql
SELECT column_name(s)
FROM table_name1
INNER JOIN table_name2 
ON table_name1.column_name=table_name2.column_name
```

##### LEFT JOIN
LEFT JOIN 关键字会从左表 (table_name1) 那里返回所有的行，即使在右表 (table_name2) 中没有匹配的行。

```sql
SELECT column_name(s)
FROM table_name1
LEFT JOIN table_name2 
ON table_name1.column_name=table_name2.column_name
```

##### RIGHT JOIN
RIGHT JOIN 关键字会右表 (table_name2) 那里返回所有的行，即使在左表 (table_name1) 中没有匹配的行。

```sql
SELECT column_name(s)
FROM table_name1
RIGHT JOIN table_name2 
ON table_name1.column_name=table_name2.column_name
```
##### FULL JOIN
返回所有行，如果有匹配则合并。

```sql
SELECT column_name(s)
FROM table_name1
FULL JOIN table_name2 
ON table_name1.column_name=table_name2.column_name
```

##### UNION
UNION 操作符用于合并两个或多个 SELECT 语句的结果集。
请注意，UNION 内部的 SELECT 语句必须拥有相同数量的列。列也必须拥有相似的数据类型。同时，每条 SELECT 语句中的列的顺序必须相同。

```sql
SELECT column_name(s) FROM table_name1
UNION
SELECT column_name(s) FROM table_name2
```
默认地，UNION 操作符选取不同的值。如果允许重复的值，请使用 UNION ALL。

```sql
SELECT column_name(s) FROM table_name1
UNION ALL
SELECT column_name(s) FROM table_name2
```
##### SELECT INTO
SELECT INTO 语句从一个表中选取数据，然后把数据插入另一个表中。
SELECT INTO 语句常用于创建表的备份复件或者用于对记录进行存档。

```sql
SELECT *
INTO new_table_name [IN externaldatabase] 
FROM old_tablename
```
#### 视图
在 SQL 中，视图是基于 SQL 语句的结果集的可视化的表。
视图包含行和列，就像一个真实的表。视图中的字段就是来自一个或多个数据库中的真实的表中的字段。我们可以向视图添加 SQL 函数、WHERE 以及 JOIN 语句，我们也可以提交数据，就像这些来自于某个单一的表。
**注释**：数据库的设计和结构不会受到视图中的函数、where 或 join 语句的影响。

```sql
CREATE VIEW view_name AS
SELECT column_name(s)
FROM table_name
WHERE condition
```

### 其他常用语句
#### AS
```sql
SELECT column_name(s)
FROM table_name
AS alias_name

SELECT column_name AS alias_name
FROM table_name
```

#### Date
- NOW()	返回当前的日期和时间
- CURDATE()	返回当前的日期
- CURTIME()	返回当前的时间
- DATE()	提取日期或日期/时间表达式的日期部分
- EXTRACT()	返回日期/时间按的单独部分
- DATE_ADD()	给日期添加指定的时间间隔
- DATE_SUB()	从日期减去指定的时间间隔
- DATEDIFF()	返回两个日期之间的天数
- DATE_FORMAT()	用不同的格式显示日期/时间

#### NULL
如果表中的某个列是可选的，那么我们可以在不向该列添加值的情况下插入新记录或更新已有的记录。这意味着该字段将以 NULL 值保存。
NULL 值的处理方式与其他值不同。

无法使用比较运算符来测试 NULL 值，比如 =, <, 或者 <>。
我们必须使用 IS NULL 和 IS NOT NULL 操作符。

```sql
SELECT LastName,FirstName,Address FROM Persons
WHERE Address IS NULL
```

```sql
SELECT ProductName,UnitPrice*(UnitsInStock+IFNULL(UnitsOnOrder,0))
FROM Products
```
## SQL 函数
### Aggregate 函数
- AVG(column)	返回某列的平均值
- COUNT(column)	返回某列的行数（不包括 NULL 值）
- COUNT(*)	返回被选行数
- FIRST(column)	返回在指定的域中第一个记录的值
- LAST(column)	返回在指定的域中最后一个记录的值
- MAX(column)	返回某列的最高值
- MIN(column)	返回某列的最低值
- STDEV(column)	 
- STDEVP(column)	 
- SUM(column)	返回某列的总和
- VAR(column)	 
- VARP(column)

	 
### Scalar 函数
- UCASE(c)	将某个域转换为大写
- LCASE(c)	将某个域转换为小写
- MID(c,start[,end])	从某个文本域提取字符
- LEN(c)	返回某个文本域的长度
- INSTR(c,char)	返回在某个文本域中指定字符的数值位置
- LEFT(c,number_of_char)	返回某个被请求的文本域的左侧部分
- RIGHT(c,number_of_char)	返回某个被请求的文本域的右侧部分
- ROUND(c,decimals)	对某个数值域进行指定小数位数的四舍五入
- MOD(x,y)	返回除法操作的余数
- NOW()	返回当前的系统日期
- FORMAT(c,format)	改变某个域的显示方式
- DATEDIFF(d,date1,date2)	用于执行日期计算

### GROUP BY
GROUP BY 语句用于结合合计函数，根据一个或多个列对结果集进行分组。

```sql
SELECT column_name, aggregate_function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name
```

### HAVING
在 SQL 中增加 HAVING 子句原因是，WHERE 关键字无法与合计函数一起使用。

```sql
SELECT column_name, aggregate_function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name
HAVING aggregate_function(column_name) operator value
```

