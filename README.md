# randomPyStuff
The repository for all my random Python projects, where I try to automate things to make it easier to do stuff and to save time. Everything here is free for use, and feedback/comments are much appreciated. Please feel free to fork and make the code your own, or even contribute new ideas to these projects! 

## Projects in the Repo
### Library Scrape
This is a script that I'm writing to check the NLB's catalogue for the books that I want to borrow. The previous approach utilised a number of book URLs in the catalogue, then 
took these URLs as well as a selected library and checked the catalogue, returning the status of books in that particular library. However, a critical issue faced is that the URL 
endpoints are dynamic and include a hash that expires after a certain amount of time, meaning that the URLs would be invalid after awhile, and would crash the scrape. The new approach 
is to login to the user account and use the list of bookmarked books to get the loan details, which circumvents the problem caused by dynamic URL endpoints. I wrote this to better understand 
how automation would work if we needed to access several pages (especially if it involved a login), and was able to use Selenium to achieve this. I also wrote this so I don't have to manually check the library's website anymore!

### Scraping project
This is a script that searches the ShareInvestor website based on a bunch of URLS and pulls the stock name and price, then exports it to an excel file. I wrote this to better understand 
how to scrape websites using BeautifulSoup. This taught me how to work with HTML code and filter out what I needed using regex.

### Credit Card Statement Checker
This was a script written to quickly count the total sum of my credit and debit transactions in my SC Spree Credit Card statement, so that I could check that the billed amount is accurate. It takes the downloadable CSV statement from the SC Banking website as an input, and returns a bunch of print statements which check that the value is correct. 

A possible extension of this project is to calculate the eligible cashback on my transactions to ensure that it corroborates with the actual cashback that I'm receiving from SC.

### DPC Schedule Scraper
A scraper to get the games being played each week in the Dota Pro Circuit (DPC), so that I don't have to manually monitor the games that I want to watch anymore. Built over [`liquipediapy`](https://github.com/c00kie17/liquipediapy), thanks `c00kie17`! Still very much in beta, there are a number of changes still to be made!