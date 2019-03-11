import xml.etree.ElementTree as ET
from datetime import date, datetime

from requests import get

from constants import EUR
from exceptions import UnknownCurrency

CBR_CURRENCY_CODES = {
    EUR: 'R01239'
}

CBR_API = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

CBR_DATE_FORMAT_IN_ARGS = '%d/%m/%Y'
CBR_DATE_FORMAT_IN_RESP = '%d.%m.%Y'

DATE = 'date'
RATE = 'rate'


class CbrApiClient:
    def __init__(self):
        pass

    def retrieve_rates_for_range(self, from_date, to_date, currency_from):
        if CBR_CURRENCY_CODES.get(currency_from) is None:
            raise UnknownCurrency(currency_from)

        if not (isinstance(from_date, date) and isinstance(to_date, date)):
            raise TypeError('Dates provided must be of datetime.date type')

        payload = {
            'date_req1': from_date.strftime(CBR_DATE_FORMAT_IN_ARGS),
            'date_req2': to_date.strftime(CBR_DATE_FORMAT_IN_ARGS),
            'VAL_NM_RQ': CBR_CURRENCY_CODES.get(currency_from)
        }

        resp = get(CBR_API, params=payload)

        return self.parse_cbr_response(resp.text)

    def parse_cbr_response(self, resp):
        root = ET.fromstring(resp)
        result = []
        for record in root:
            date_value = record.attrib.get('Date')
            for elem in record:
                if elem.tag == 'Value':
                    rate = elem.text.replace(',', '.')
                    result.append({
                        DATE: datetime.strptime(date_value, CBR_DATE_FORMAT_IN_RESP).date(),
                        RATE: float(rate)
                    })
        return result
