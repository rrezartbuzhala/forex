create database Forliza
go
use Forliza;
CREATE TABLE Analysts (
	Id uniqueidentifier primary key ,
	Username nvarchar(50) not null,
	Fullname nvarchar(50) not null,
)
CREATE TABLE AnalystTweets (
	Id UNIQUEIDENTIFIER primary key not null,
	Analyst_Id UNIQUEIDENTIFIER not null,
	foreign key (Analyst_Id) references Analysts(Id),
	Tweet nvarchar(280) not null,
	Added_At int not null IDENTITY(1,1),
)

CREATE TABLE Keywords(
	Id UNIQUEIDENTIFIER primary key not null ,
	Keyword nvarchar(30) not null,

)
CREATE TABLE KeywordsInTweets (
	Tweet_Id UNIQUEIDENTIFIER not null,
	Keyword_Id UNIQUEIDENTIFIER not null

)


INSERT INTO Analysts VALUES(NEWID(),'forexanalyst','ForexAnalyst.com')
INSERT INTO Analysts VALUES(NEWID(),'MXInvesting','MX investing (Forex Signals)')
INSERT INTO Analysts VALUES(NEWID(),'Rrezart_Buzhala','Rrezart Buzhala')
INSERT INTO Analysts VALUES(NEWID(),'altinsallauka','Altin Sallauka')

INSERT INTO Keywords VALUES(NEWID(),'sell')
INSERT INTO Keywords VALUES(NEWID(),'buy')





GO
CREATE PROCEDURE InsertTweets @Id uniqueidentifier, @Analyst_Id uniqueidentifier, @Tweet nvarchar(280)
AS
BEGIN
    insert into AnalystTweets values(@Id, @Analyst_Id, @Tweet)
END;

GO
CREATE PROCEDURE InsertTweetsWithKeywords @Tweet_Id UNIQUEIDENTIFIER, @Keyword_Id UNIQUEIDENTIFIER
AS
BEGIN
    insert into KeywordsInTweets values(@Tweet_Id,@Keyword_Id)
END;