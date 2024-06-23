# Dependencies

- [Python 3.10.6](https://www.python.org/)
- [Scrapy](https://scrapy.org/)
- [Selenium](https://www.selenium.dev/)

# Usage

To run a single spider: 

`scrapy crawl <spider Name> -o output/<file name>.jsonl`

See [scrapy docs](https://docs.scrapy.org/en/latest/index.html) for more info

# Stores

## Shopify
- [x] ABU
- [x] Abena (missing products)
- [x] Bambino
- [x] Crinklz
- [x] CutiePlusU
- [x] Kiddo Diapers
- [x] Kitnitiative
- [x] LandOfGenie
- [x] LilComforts
- [x] LNGU
- [x] PretendAgain
- [x] The Cuddle Cooperative
- [x] Tykables

## Amazon
- [ ] Aimisin
- [ ] SUNKISS
- [ ] The ABDL Shop (also theabdlshop.com)
- [ ] Trest (also trestcare.com)

## Misc
- [x] AwwSoCute
- [ ] Ageplay Outfitters (ebay)
- [x] InControl (needs work)
- [ ] LittleForBig
- [ ] Molicare
- [ ] Northshore (needs Selenium)
- [ ] NRU 
- [x] Rearz (needs work)

## Resellers
- [ ] ABdlr
- [ ] Amazon
- [ ] MyDips
- [ ] MyInnerBaby (Shopify)
- [ ] The ABDL Company
- [ ] The ABDL Littles' Shop
- [ ] XPMedical

# Todo
- Add tape types (hook and loop, adhesive, etc.)
- Properly handle sales for most stores
- Make Rearz / InControl not slow
- Complete Abena
- Parallelize spiders?