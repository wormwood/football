USE [fixtures]
GO

/****** Object:  Table [dbo].[bets]    Script Date: 13/10/2018 16:02:23 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[bets](
	[Column 0] [varchar](50) NULL,
	[FixtureID] [varchar](50) NULL,
	[season] [varchar](50) NULL,
	[leagueid] [varchar](50) NULL,
	[fixDate] [varchar](50) NULL,
	[HomeTeamID] [varchar](50) NULL,
	[FTHG] [varchar](50) NULL,
	[AwayTeamID] [varchar](50) NULL,
	[FTAG] [varchar](50) NULL,
	[HomeELO_prev] [varchar](50) NULL,
	[AwayELO_prev] [varchar](50) NULL,
	[HomeTeamResult] [varchar](50) NULL,
	[AwayTeamResult] [varchar](50) NULL,
	[HomeTeam] [varchar](50) NULL,
	[AwayTeam] [varchar](50) NULL,
	[FTHG_3] [varchar](50) NULL,
	[FTAG_3] [varchar](50) NULL,
	[FTHG_5] [varchar](50) NULL,
	[FTAG_5] [varchar](50) NULL,
	[HomeOdds] [varchar](50) NULL,
	[DrawOdds] [varchar](50) NULL,
	[AwayOdds] [varchar](50) NULL,
	[FixtureDateAsDate] [varchar](50) NULL,
	[Target] [varchar](50) NULL,
	[HTRecord] [varchar](50) NULL,
	[ATRecord] [varchar](50) NULL,
	[ExpectedResult] [varchar](50) NULL,
	[FTG_3] [varchar](50) NULL,
	[FTG_5] [varchar](50) NULL,
	[clf_prediction] [varchar](50) NULL
) ON [PRIMARY]
GO

