// test with "node PriceScraper.js" in the terminal

const axios = require('axios');
const cheerio = require('cheerio');
const cron = require('node-cron');

const url = 'https://www.amazon.com/Hiware-12-piece-Stainless-Teaspoon-Inches/dp/B01D9OS5KA/';
const id = '#price_inside_buybox';

async function scrapePrice() {
    const {data: html} = await axios.get(url).catch(() => {
        console.log("Error: Could not get page");
    });
    const page = cheerio.load(html);                                
    const priceString = page(id).text().trim();                     
    const priceNumber = parseFloat(priceString.replace('$', ''));
    console.log(priceNumber); 
}

// Right now this scrapes the page every 5 seconds for testing purposes. The scheduling time will be changed later.
cron.schedule('*/5 * * * * *', async() => {
    scrapePrice();
});