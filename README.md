# Scrapping
Repository to publish and store mine web-scrapings, which might be useful for the common audience. The titles of each section refers to each scraper (made in Pyhton using Beautiful Soup and Selenium).

## ANEEL - Electricity
ANEEL stands for Agência Nacional de Energia Elétrica, the provider of the Consumer Units per City (Unidades Consumidoras por Município) data. The script [scraping_aneel](https://github.com/Vilmar1/my-scrappings/blob/main/scraping_aneel.py) aims to collect this value for all brazilian cities. 

In the code, the first section collects the number of cities in each state, useful to make the counters in the next part. The second section scrapes the last 11 years of data with 11 navigators, stored in a DataFrame.  

<p align="center">
  <img src="https://user-images.githubusercontent.com/38505459/185278775-ad02dc73-d366-4583-bd56-086b7f2da128.png" width="700">
</p>

## Nightlight Satellite Imagery
The Suomi National Polar-orbiting Partnership (or Suomi NPP) satellite collects the radiation in the earth daily. Next, it sends this information to the US National Oceanic and Atmospheric Administration (NOAA), generating the VIIRS database. See more details in https://eogdata.mines.edu/products/vnl/.

<p align="center">
  <img src="https://user-images.githubusercontent.com/38505459/185278031-9df3c9f9-d81c-4acd-a4cd-c49b2fa27a40.png" width="400">
</p>

The script [scraping_eog](https://github.com/Vilmar1/my-scrappings/blob/main/scraping_eog.py) collects daily two products of NOAA: the nighlights VIIRS images in Brazil (in the function ```download_imgs()``` ) and the the VIIRS Cloud Mask, an image with the probability of cloudiness in each pixel (this part relates to the function ```download_mask()```).

<p align="center">
   <img src="https://user-images.githubusercontent.com/38505459/185278463-44162138-0295-42a0-ba16-26d27a5dae7b.png" width="700">
</p>

