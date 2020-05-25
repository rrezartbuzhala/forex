/****** Execute this first... ******/
CREATE TABLE Analysts (
	Id uniqueidentifier primary key default NEWID(),
	Username nvarchar(50) not null,
	Fullname nvarchar(50) not null,
	Source nvarchar(200)
)

INSERT INTO Analysts VALUES(NEWID(),'forexanalyst','ForexAnalyst.com','Twitter')
INSERT INTO Analysts VALUES(NEWID(),'MXInvesting','MX investing (Forex Signals)','Twitter')

CREATE TABLE AnalystTweets (
	Id int not null primary key IDENTITY(1,1),
	AnalystID UNIQUEIDENTIFIER not null,
	foreign key (AnalystID) references Analysts(Id),
	Tweet nvarchar(280) not null
)

/****** ...and this second ******/
CREATE PROCEDURE InsertTweets @AnalystID uniqueidentifier, @Tweet nvarchar(280)
AS
BEGIN
    insert into AnalystTweets values(@AnalystID, @Tweet)
END;