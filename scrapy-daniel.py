import scrapy


class Spider12(scrapy.Spider):
    
    name = 'spider12'
    
    allowed_domains = ['pagina12.com.ar']
    
    custom_settings = { 'FEED_FORMAT' : 'json',
                      'FEED_URI' : 'resultados.json',
                      'DEPTH_LIMIT':2}
    
    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                 'https://www.pagina12.com.ar/secciones/economia',
                 'https://www.pagina12.com.ar/secciones/sociedad',
                 'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                 'https://www.pagina12.com.ar/secciones/deportes',
                 'https://www.pagina12.com.ar/secciones/el-mundo',
                 'https://www.pagina12.com.ar/secciones/universidad-diario']
    
    def parse(self,response):
        
        #listado de notas
        
        notas = response.xpath('//div[@class="articles-list"]//article[@class="article-item article-item--teaser"]//a/@href').getall()
        
        for nota in notas:
            
            yield response.follow(nota, callback = self.parse_nota)
        
        # link de pagina siguiente
        
        next_page = response.xpath('//a[@class="next"]/@href')
        
        if next_page is not None:
            
            yield response.follow(next_page, callback=self.parse)
            
    def parse_nota(self, response):
        
        #parseo de notas
        
        titulo = response.xpath('//div[@class="col 2-col"]/h4/text()').get()
        
        cuerpo = ''.join(response.xpath('//div[@class="col 2-col"]/p/text()').getall())
        
        yield{'url':response.url,
             'titulo':titulo,
             'cuerpo':cuerpo}


from scrapy.crawler import CrawlerProcess
process = CrawlerProcess()
process.crawl(Spider12)
process.start()