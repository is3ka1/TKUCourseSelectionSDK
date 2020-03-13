from parsel import Selector


def parse_data(html: str) -> dict:
    sel = Selector(html)
    data = {
        prop: sel.css(f'#{prop}::text').get().strip()
        for prop in ('lblHead', 'lblStuNo', 'lblChName', 'lblDeptNm', 'lblStatus')
    }

    data.update({
        'msg': ''.join(sel.xpath('//form/div/table/tr[2]/td[3]//text()').getall()).strip(),
        'course_info_queried': _parse_table(
            sel.xpath('//form/div/table/tr[3]/td[2]/font[2]/preceding-sibling::div/table')),
        'elective_info': _parse_table(
            sel.xpath('//form/div/table/tr[3]/td[2]/font[2]/following-sibling::div/table')),
        'subtotal': ''.join(sel.xpath('//form/div/table/tr[4]//text()').getall()).strip()
    })
    return data


def _parse_table(table: Selector):
    column_names = [''.join(col.css('::text').getall())
                    for col in table.xpath('tr[1]/th')]
    rows = [[''.join(item.css('::text').getall()).strip() for item in row.xpath('td')]
            for row in table.xpath('tr[position() > 1]')]
    return [dict(zip(column_names, row)) for row in rows]
