# PropScout

The PropScout app is a simple to use app created for property investors to help them identify promising markets as well as simplify the process of property deal analysis.

## State of Development

- property alerts sent to gmail account are parsed using google gmail API
- html copy of page stored in SQLite database
- property specs are extracted from the html and parsed to json format and recommitted to database
- daily script created to run everyday and add properties to the database

## Next Step

- take the data from json to dataframe for property analysis
- once analysed the results should be stored somewhere for reference
- would like visualisation of the properties on a map and the ability to click on them to see more information
- also want the dashboard to indicate properties that meet investment criteria
