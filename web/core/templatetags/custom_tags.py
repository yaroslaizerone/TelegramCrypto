from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_active(context, url_name):
    if context['request'].resolver_match.url_name == url_name:
        return 'active'
    return ''

@register.simple_tag
def checked_column(column_name, has_data):
    """ Тег используется для автоматической установки чекбокса для столбца в таблице. """
    if has_data.get(column_name):
        return 'checked'
    return ''


@register.simple_tag(takes_context=True)
def export_excel_url(context):
    request = context['request']
    params = []

    if request.GET.getlist('region'):
        for region in request.GET.getlist('region'):
            params.append(f'region={region}')
    if request.GET.getlist('utc'):
        for utc in request.GET.getlist('utc'):
            params.append(f'utc={utc}')
    if request.GET.get('max_rows'):
        params.append(f'max_rows={request.GET.get("max_rows")}')
    if request.GET.get('gender'):
        params.append(f'gender={request.GET.get("gender")}')
    if request.GET.get('tag'):
        params.append(f'tag={request.GET.get("tag")}')
    for column in request.GET.getlist('columns'):
        params.append(f'columns={column}')

    params.append('export=excel')
    return f"{request.path}?{'&'.join(params)}"
