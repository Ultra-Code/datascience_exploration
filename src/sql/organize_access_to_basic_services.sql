DROP TABLE IF EXISTS Basic_Services;
DROP TABLE IF EXISTS Economic_Indicators;
DROP TABLE IF EXISTS Geographic_Location;



/* Create Geographic_Location Table */
CREATE TABLE united_nations.Geographic_Location (
  Country_name VARCHAR(37) PRIMARY KEY,
  Sub_region VARCHAR(25),
  Region VARCHAR(32),
  Land_area NUMERIC(10,2));

/* Adding data */
INSERT INTO united_nations.Geographic_Location (Country_name, Sub_region,Region, Land_area)
SELECT Country_name
      ,Sub_region
      ,Region
      ,AVG(Land_area) as Country_area
FROM united_nations.Access_to_Basic_Services
GROUP BY Country_name
        ,Sub_region
        ,Region;


/* Create Economic_Indicators Table */
CREATE TABLE united_nations.Economic_Indicators (
  Country_name VARCHAR(37),
  Time_period INTEGER,
  Est_gdp_in_billions NUMERIC(8,2),
  Est_population_in_millions NUMERIC(11,6),
  Pct_unemployment NUMERIC(5,2),
  PRIMARY KEY (Country_name, Time_period),
  FOREIGN KEY (Country_name) REFERENCES Geographic_Location (Country_name));

/* Adding data */
INSERT INTO Economic_Indicators (Country_name, Time_period, Est_gdp_in_billions, Est_population_in_millions, Pct_unemployment)
SELECT Country_name
      ,Time_period
      ,Est_gdp_in_billions
      ,Est_population_in_millions
      ,Pct_unemployment
FROM united_nations.Access_to_Basic_Services;


/* Create Basic_Services Table */
CREATE TABLE united_nations.Basic_Services (
  Country_name VARCHAR(37),
  Time_period INTEGER,
  Pct_managed_drinking_water_services NUMERIC(5,2),
  Pct_managed_sanitation_services NUMERIC(5,2),
  PRIMARY KEY (Country_name, Time_period),
  FOREIGN KEY (Country_name) REFERENCES Geographic_Location (Country_name)
);
/* Adding data */
    INSERT INTO Basic_Services (Country_name, Time_period, Pct_managed_drinking_water_services, Pct_managed_sanitation_services)
    SELECT Country_name
          ,Time_period
          ,Pct_managed_drinking_water_services
          ,Pct_managed_sanitation_services
    FROM united_nations.Access_to_Basic_Services
