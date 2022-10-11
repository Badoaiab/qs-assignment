-- This is where you will write the SQL to create the tables needed by the bar staff to assist on restocking decisions

DROP VIEW IF EXISTS glassPerBars;
DROP VIEW IF EXISTS dailyBarsRevenue;
DROP VIEW IF EXISTS dailyBarsSales;
DROP VIEW IF EXISTS dailyBarsUsedGlasses;
DROP VIEW IF EXISTS stockVsUsedGlasses;


CREATE VIEW glassPerBars AS SELECT GlassType, Stock, Bar from allGlass Group By GlassType, Bar;  --Helps in terms of visualisation, each glass type is now easily seen against all the bars

CREATE VIEW dailyBarsRevenue AS SELECT TransDate, Bar, Round(SUM(Price)) as Revenue from allTransactions Group By Bar,TransDate; --allows the bar staff to see the total revenue for each day

CREATE VIEW dailyBarsSales AS Select Count(Drink),Drink, TransDate, Bar from allTransactions Group By TransDate, Drink, Bar; -- allows the bar staff to see the number of drinks sold per type

CREATE VIEW dailyBarsUsedGlasses AS SELECT Count(GlassType) AS GlassesUsed, GlassType, Bar, TransDate From drinkGlassPair Inner Join allTransactions ON drinkGlassPair.Drink = allTransactions.Drink Group By GlassType, TransDate, Bar; -- Can see how many of each type of glass was used per day

CREATE VIEW stockVsUsedGlasses AS SELECT b.Stock, a.GlassesUsed, a.GlassType, b.Bar, a.TransDate From dailyBarsUsedGlasses AS a Inner Join glassPerBars AS b ON a.GlassType = b.GlassType AND a.Bar = b.Bar Order By a.TransDate; --Shows how many glasses a bar has vs how many were used on a day

--Some exampels of queries:
--Select Count(Drink),Drink, TransDate, Bar from allTransactions Where Bar = "NewYork" Group By TransDate, Drink, Bar;   --in order to see the number of drinks sold in NewYork or even better can query the view "dailyBarsSales"

