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