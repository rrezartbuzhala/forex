/****** Execute this first... ******/
CREATE TABLE Analysts (
	Id uniqueidentifier primary key ,
	Username nvarchar(50) not null,
	Fullname nvarchar(50) not null,
)
CREATE TABLE AnalystTweets (
	Analyst_Id UNIQUEIDENTIFIER not null,
	foreign key (AnalystID) references Analysts(Id),
	Tweet nvarchar(280) not null,
	Tweet_Id nvarchar(MAX) primary key not null,
	Added_At int not null IDENTITY(1,1),
)

CREATE TABLE KeywordsInTweets (
	Tweet_Id nvarchar(MAX) foreign key REFERENCES AnalystTweets(Tweet_Id) not null,
	Keyword nvarchar(30) foreign key REFERENCES Keywords(Keyword) not null,
)
CREATE TABLE Keywords(
	Keyword nvarchar(30) not null,
)

INSERT INTO Analysts VALUES(NEWID(),'forexanalyst','ForexAnalyst.com')
INSERT INTO Analysts VALUES(NEWID(),'MXInvesting','MX investing (Forex Signals)')
INSERT INTO Analysts VALUES(NEWID(),'Rrezart_Buzhala','Rrezart Buzhala')



GO
CREATE PROCEDURE InsertTweets @AnalystID uniqueidentifier, @Tweet nvarchar(280), @Tweet_Id uniqueidentifier
AS
BEGIN
    insert into AnalystTweets values(@AnalystID, @Tweet,@Tweet_Id)
END;

GO
CREATE PROCEDURE InsertTweetsWithKeywords @Tweet_Id uniqueidentifier, @Keyword nvarchar(30)
AS
BEGIN
    insert into KeywordsWithTweets values(@Tweet_Id,@Keyword)
END;