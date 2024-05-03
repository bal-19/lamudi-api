from bs4 import BeautifulSoup
import requests


class Lamudi:
    def __init__(self, url, fillter, keyword, total_pages):
        self.url = url
        self.filter = fillter
        self.keyword = keyword
        self.total_pages = total_pages
    
    def get_data(self):
        try:
            url = self.url
            total_data = 0
            content = []
            while url:
                current_page = int(url.split('&page=')[-1])
                if current_page > self.total_pages:
                    break
                
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'})
                status_code = r.status_code
                soup = BeautifulSoup(r.text, "html.parser")
                
                for kios in soup.select('body > div.row.fullWidth.ClpBody > div.small-9.columns.js-listingContainer > div.clp-wrapper > div:nth-child(2) > div.row.ListingCell-row.ListingCell-agent-redesign'):
                    title = kios.select_one('div > div.ListingCell-AllInfo.ListingUnit > a > div.ListingCell-TitleWrapper > div > h3')
                    if title:
                        title = title.text.strip()
                    
                    address = kios.select_one('div > div.ListingCell-AllInfo.ListingUnit > a > div.ListingCell-TitleWrapper > div > div > span.ListingCell-KeyInfo-address-text')
                    if address:
                        address = address.text.strip()
                    
                    desc = kios.select_one('div > div.ListingCell-AllInfo.ListingUnit > a > div.ListingCell-shortDescription')
                    if desc:
                        desc = desc.text.strip()
                    
                    price = kios.select_one('div > div.ListingCell-AllInfo.ListingUnit > a > div.ListingCell-KeyInfo-price > div.ListingCell-KeyInfo-PriceWrapper > span')
                    if price:
                        price = price.text.strip()
                        
                    attributes = []
                    for attr in kios.select('div > div.ListingCell-AllInfo.ListingUnit > a > div.ListingCell-KeyInfo-price > div.ListingCell-keyInfo-details > div > div'):
                        name = attr.select_one('span.KeyInformation-label_v2').text.strip().lower().replace(' ', '_')
                        value = attr.select_one('div.KeyInformation-description_v2 > span.KeyInformation-value_v2').text.strip()
                        attributes.append({name: value})
                
                    detail_link = kios.select_one('div > div.ListingCell-AllInfo.ListingUnit > div > div > div:nth-child(1) > a').get('href')
                    details = self.get_detail_data(detail_link)
                    details['attributes'] = attributes

                    
                    content.append({
                        'title': title,
                        'address': address,
                        'desc': desc,
                        'price': price,
                        'details': details
                    })
                    
                    total_data += 1
                
                next_page = url.replace('page=' + str(current_page), 'page=' + str(current_page + 1))
                if next_page:
                    url = next_page

            data = {
                "status": status_code,
                "url": url.split('&')[0],
                "filter": self.filter,
                "keyword": self.keyword,
                "content": content,
                "total_data": total_data, 
                "total_pages": self.total_pages,
            }
            
            return data

        except Exception as e:
            data = {
                "status": r.status_code,
                "url": url,
                "filter": filter,
                "keyword": self.keyword,
                "error": str(e)
            }
            
            return data
        
    def get_detail_data(self, url):
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'})
            soup = BeautifulSoup(r.text, "html.parser")
            
            # AGENT INFO
            agent_name = soup.select_one('body > div.PdpV5-container > div.PdpV5-content > div.PdpV5-content-sidebarColumn.js-ContainerSideColumn > div.AgentInfoV2-wrapper > div.AgentInfoV2-column > div.AgentInfoV2-leftColumn > div.AgentInfoV2-agentSection > div > div.AgentInfoV2-agent-details-wrapper > div.AgentInfoV2-agent-name')
            if agent_name:
                agent_name = agent_name.text.strip()
            
            agent_agency = soup.select_one('body > div.PdpV5-container > div.PdpV5-content > div.PdpV5-content-sidebarColumn.js-ContainerSideColumn > div.AgentInfoV2-wrapper > div.AgentInfoV2-column > div.AgentInfoV2-leftColumn > div.AgentInfoV2-agentSection > div > div.AgentInfoV2-agent-details-wrapper > div.AgentInfoV2-agent-agency > a')
            if agent_agency:
                agent_agency = agent_agency.text.strip()
            
            agent_since = soup.select_one('body > div.PdpV5-container > div.PdpV5-content > div.PdpV5-content-sidebarColumn.js-ContainerSideColumn > div.AgentInfoV2-wrapper > div.AgentInfoV2-column > div.AgentInfoV2-leftColumn > div.AgentInfoV2-agentSection > div > div.AgentInfoV2-agent-details-wrapper > div.AgentInfoV2-agent-verified-wrapper > div > div.agent-member-since')
            if agent_since:
                agent_since = agent_since.text.strip()
            
            agent_phone = soup.select_one('#js-viewerContainerSuccessOverlay > div > div > div.LeadSuccess-content > div.LeadSuccess-phone > div.js-RequestPhoneForm-showPhoneAgentInfo-mobile.show > span')
            if agent_phone:
                agent_phone = agent_phone.text.strip()
            
            agent_medias = []
            medias = soup.select('body > div.PdpV5-container > div.PdpV5-content > div.PdpV5-content-sidebarColumn.js-ContainerSideColumn > div.AgentInfoV2-wrapper > div.AgentInfoV2-column > div.AgentInfoV2-leftColumn > div.AgentInfoV2-agentSection > div > div.AgentInfoV2-agent-logo-wrapper > img')
            if medias:
                for agent_media in medias:
                    agent_medias.append(agent_media.get('src'))
                
            data = {
                'detail_agent': {
                    'name': agent_name,
                    'agency': agent_agency,
                    'since': agent_since,
                    'phone': agent_phone,
                    'medias': agent_medias
                },
                'attributes': None
            }
            
            return data
            
        except Exception as e:
            data = {
                "url": url,
                "error": str(e)
            }
        
            return data
