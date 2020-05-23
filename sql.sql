
CREATE TABLE Analysts (
	Username nvarchar(50) not null,
	Fullname nvarchar(50) not null,
)

INSERT INTO Analysts VALUES('forexanalyst','ForexAnalyst.com')
INSERT INTO Analysts VALUES('MXInvesting','MX investing (Forex Signals)')

CREATE TABLE AnalystTweets (
	Username nvarchar(50) not null,
	Fullname nvarchar(50) not null,
	Tweet nvarchar(280) not null
)


CREATE PROCEDURE InsertTweets @Username nvarchar(50), @Fullname nvarchar(50), @Text nvarchar(280)
AS
BEGIN
    insert into AnalystTweets values(@Username, @Fullname, @Text)
END;