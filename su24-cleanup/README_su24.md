# Spark!-NCF-Summer24-cleanup-repo

Hi there! My name is Woohyeon Her, and I am a technical intern for data science for Spark! I worked on the NCF project for the summer of 2024.

This folder contains 2 ipynb files and a folder that contains all the csv files and graphs produced from the ipynb files.

### scrapping.ipynb

scrapping.ipynb is a file that I worked on to scrap data from Foundation Maps by Candid (https://maps.foundationcenter.org/#/map/?subjects=all&popgroups=all&years=2020,2021,2022,2023,2024&location=6252001&excludeLocation=0&geoScale=ADM0&layer=geo_area&boundingBox=-152.666,17.056,-43.33,58.631&gmOrgs=all&recipOrgs=all&tags=all&keywords=&pathwaysOrg=&pathwaysType=&acct=raceequpopup&typesOfSupport=all&transactionTypes=all&amtRanges=all&minGrantAmt=0&maxGrantAmt=0&gmTypes=all&recipTypes=all&minAssetsAmt=0&maxAssetsAmt=0&minGivingAmt=0&maxGivingAmt=0&andOr=0&includeGov=1&custom=all&customArea=all&indicator=&dataSource=oecd&chartType=trends&multiSubject=1&listType=gm&windRoseAnd=undefined&zoom=4). It contains all the approaches I took. The Foundation Map provides data in 3 different layers for Funders section and Recipients section, and 2 layers for Grants section.

First, I started off by writing code to scrap first layers of three sections. However, it turned out many data were repeated, so I shifted focus to scraping only the 2nd layer. I worked to get Funders data and Recipients data, and my teammate Tami worked to gather Grants data. Due to this, if you want to look at how Grants data was collected, it is best to look at her ipynb file. Mine is for the other two.

Due to the nature of the question, Funders data and Recipients data were not used. Instead, Grants data was used to answer the questions.

### EDA.ipynb

EDA.ipynb is a file that I worked to answer questions from the client, NCF. For the specific questions, refer to the project description. I answered questions 1, 2, 6, 7, and 9. The file contains all the approaches I took to answer the questions. You would have to adjust file directory to

### data-collection

data-collection is a folder that contains all the CSV files and graphs I produced from EDA.ipynb. It also contains the whole grant data, which was used most of the time.
