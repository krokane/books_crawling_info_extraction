#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 19:54:38 2025

@author: kevin
"""

import scrapy

class t11_Spider(scrapy.Spider):
    name = "task11"
    start_urls = ["https://openlibrary.org/trending/forever"]
    rank = 1

    def parse(self, response):
        for book in response.css("div.details"):
            if self.rank <= 100:
                yield {
                    "title": book.css("a.results::text").get(),
                    "author": book.css("span.bookauthor a::text").get(),
                    "rank": self.rank,
                    "url": response.urljoin(book.css("a.results::attr(href)").get())
                }
                
                self.rank+=1
        
        next_page = response.css("div.pager a.ChoosePage:last-of-type::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class t12_Spider(scrapy.Spider):
    name = "task12"
    start_urls = ["https://openlibrary.org/trending/forever"]
    rank = 1
    
    def parse(self, response):
        for book in response.css("div.details"):
            if self.rank <= 100:
                title = book.css("a.results::text").get()
                author = book.css("span.bookauthor a::text").get()
                published_year = int(response.css("span.resultDetails span::text").get().split()[-1])
                url = response.urljoin(book.css("a.results::attr(href)").get())
                self.rank+=1
        
            yield response.follow(url, self.parse_book, meta = {"title":title,"author":author,"published_year":published_year})
        
        next_page = response.css("div.pager a.ChoosePage:last-of-type::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        title = response.meta['title']
        author = response.meta['author']
        published_year = response.meta['published_year']
        
        yield {
            "title": title,
            "author": author,
            "genres": [genre.strip() for genre in response.xpath("//span[contains(., 'Genres')]").css("span.reviews__value::text").getall()],
            "description": response.css("div.read-more__content p::text").get().strip(),
            "published_year": published_year
            }
        
class t13_Spider(scrapy.Spider):
    name = "task13"
    start_urls = ["https://openlibrary.org/trending/forever"]
    rank = 1
    
    def parse(self, response):
        for book in response.css("div.details"):
            if self.rank <= 100:
                author = book.css("span.bookauthor a:first-child::text").get()
                url = response.urljoin(book.css("span.bookauthor a:first-child::attr(href)").get())
                self.rank+=1
        
            yield response.follow(url, self.parse_author, meta = {"author":author})
        
        next_page = response.css("div.pager a.ChoosePage:last-of-type::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        author = response.meta['author']
        birthDate = response.css("span[itemprop='birthDate']::text").get()
        deathDate = response.css("span[itemprop='deathDate']::text").get()
        biography = response.css("div[itemprop='description'] p::text").get()
        wiki = response.css("div.profile-icon-container a:first-child::attr(href)").get()
        
        if (birthDate != None) and (deathDate != None) and (biography != None):
            yield {
                    "author": author,
                    "birthDate":birthDate,
                    "deathDate":deathDate,
                    "biography":biography
                }
        elif wiki == None:
            yield {
                "author": author,
                "birthDate":birthDate,
                "deathDate":deathDate,
                "biography":biography
                }
        else:
            yield response.follow(wiki, self.parse_wiki, meta = {"author": author, "birthDate":birthDate, "deathDate":deathDate, "biography":biography})
    
    def parse_wiki(self, response):
        author = response.meta['author']
        birthDate = response.meta['birthDate']
        deathDate = response.meta['deathDate']
        biography = response.meta['biography']
        
        #need birthDate, deathDate, and biography
        if birthDate == None:
            birthDate = response.css("span.bday::text").get()
        if deathDate == None:
            deathDate = response.xpath("//th[contains(.,'Died')]").css("td.infobox-data::text").get()
        if biography == None:
            biography = response.css("div[class='mw-content-ltr mw-parser-output'] p:first-of-type *::text").getall()
            biography = "".join(biography)
        
        yield {
            "author": author,
            "birthDate":birthDate,
            "deathDate":deathDate,
            "biography":biography
            }
    

