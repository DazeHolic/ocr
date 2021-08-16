CREATE TABLE [cache](
  [time] INTEGER,
  [status] INTEGER,
  [name] VARCHAR(30));

CREATE TABLE [o_template](
  [name1] VARCHAR(30) NOT NULL,
  [name2] VARCHAR(30) NOT NULL,
  [field1] VARCHAR(30),
  [position1] INT,
  [field2] VARCHAR(30),
  [position2] INT,
  [field3] VARCHAR(30),
  [position3] INT,
  [field4] VARCHAR(30),
  [position4] INT,
  [field5] VARCHAR(30) NOT NULL,
  [field6] VARCHAR(30) NOT NULL,
  [type] INT NOT NULL);

CREATE TABLE [result](
  [img_name] VARCHAR(30) NOT NULL,
  [name1] VARCHAR(30) NOT NULL,
  [name2] VARCHAR(30) NOT NULL,
  [field5] VARCHAR(30),
  [field6] VARCHAR(30),
  [result] VARCHAR(30),
  [type] INTEGER NOT NULL,
  [create_time] DATETIME NOT NULL,
  [update_time] DATETIME NOT NULL);

CREATE TABLE [template](
  [name1] VARCHAR(30) NOT NULL,
  [name2] VARCHAR(30) NOT NULL,
  [field1] VARCHAR(30),
  [position1] INT,
  [field2] VARCHAR(30),
  [position2] INT,
  [field3] VARCHAR(30),
  [position3] INT,
  [field4] VARCHAR(30),
  [position4] INT,
  [field5] VARCHAR(30) NOT NULL,
  [field6] VARCHAR(30) NOT NULL,
  [type] INT NOT NULL);

