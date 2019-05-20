USE [master]
GO

CREATE DATABASE [olx]
GO

USE [olx]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Apartment](
	[PostingID] [int] IDENTITY(1,1) NOT NULL,
	[price_usd] [int] NULL,
	[title] [nvarchar](4000) NULL,
	[text] [text] NULL,
	[total_area] [int] NULL,
	[kitchen_area] [int] NULL,
	[living_area] [int] NULL,
	[location] [nvarchar](255) NULL,
	[number_of_rooms] [int] NULL,
	[added_on] [date] NULL
) ON [PRIMARY]
GO
