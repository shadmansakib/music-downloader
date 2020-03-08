from bs4 import BeautifulSoup


class Soup:
    def __init__(self, html_doc, parser='html.parser'):
        self.soup = BeautifulSoup(html_doc, parser)

    def get_soup(self):
        return self.soup

    def get_all_tags(self):
        return [tag.name for tag in self.soup.find_all()]

    def get_first_tag(self):
        return self.get_all_tags()[0]

    def scrape(self, query):
        if not isinstance(query, dict) and isinstance(query, list):
            return

        result_list = []

        _content_selector = query.get('content_selector', None)
        _content_data_config = query.get('content_data')

        # get a list of all contents is content selector exists
        if _content_selector is None:
            return

        _content_list = self.soup.select(_content_selector)

        # loop through the list and scrape each data
        for _content in _content_list:
            _result_dict = {}

            # scrape data according to "content_data" config list
            for conf in _content_data_config:
                _conf_key = conf.get('name')
                _conf_selector = conf.get('selector', None)

                # for nested scraping
                _conf_scrape_nested = conf.get("scrape_config", None)

                _conf_get_as = conf.get('get_as', None)
                _conf_get_attr = conf.get('get_attr', None)
                _conf_append_url = conf.get('append_url', None)

                # scrape
                _conf_result = None
                if _conf_selector is None and _conf_scrape_nested:
                    _conf_result = self.scrape(_conf_scrape_nested)

                elif _conf_selector is not None:
                    if _conf_selector == "*":
                        if _conf_get_as == 'text':
                            _conf_result = _content.text.strip()

                        if _conf_get_attr:
                            _conf_result = _content.get(_conf_get_attr)

                        if _conf_get_attr == "href" and _conf_append_url:
                            _conf_result = '{}{}'.format(_conf_append_url.strip('/'), _conf_result)

                    else:
                        _conf_result = _content.select_one(_conf_selector)

                        if len(_conf_result) > 0:
                            _conf_result = _conf_result[0]
                            if _conf_get_as == 'text':
                                _conf_result = _conf_result.text.strip()

                            if _conf_get_attr:
                                _conf_result = _conf_result.get(_conf_get_attr)

                            if _conf_get_attr == "href" and _conf_append_url:
                                _conf_result = '{}{}'.format(_conf_append_url.strip('/'), _conf_result)
                        else:
                            _conf_result = None

                # make a result dict
                _result_dict.update({
                    _conf_key: _conf_result
                })

            # end of "for conf in _content_data_config: ..."

            # append/extend result list
            result_list.append(_result_dict)

        # end of "for _content in _content_list: ..."
        return result_list

    # end of "select_content_as_dict()"
