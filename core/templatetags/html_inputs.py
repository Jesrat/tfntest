import html
from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def datatables_thead(context):
    val = [[v for k, v in i.items() if k == 'title'][0] for i in context['model'].html_table['td']]
    ths = HtmlList([HtmlElement('th', [('scope', 'col')], i, escape=True) for i in val])
    # noinspection PyProtectedMember
    if 'delete' in context['model'].html_table.get('controls', []):
        # noinspection PyProtectedMember
        if context['request'].user.has_perm('%(app_label)s.delete_%(model_name)s' % context['model']._meta.__dict__):
            ths.append(HtmlElement('th', [], 'Actions'))
    return mark_safe(HtmlElement('thead', [], ths).html)


# noinspection PyUnusedLocal
@register.simple_tag(takes_context=True)
def datatables_endpoint(context):
    # noinspection PyProtectedMember
    return reverse('api:%(model_name)s-list' % context['model']._meta.__dict__)


@register.simple_tag(takes_context=True)
def datatables_columns(context):
    """
    result should be somthing like this:
    [
        {data: "id", "render": (data, type, row, meta)=>{return '<a class="btn-link" href="/noc/ips/'+data+'/edit/">'+data+'</a>';}},
        {data: "ip"},
        {data: "name"},
        {data: "", "render": (data, type, row, meta)=>{return '<a class="btn btn-danger delete-item" href="/api/fw/ips/'+data+'/"><i class="fas fa-trash-alt"></i></a>';}},
    ]
    """

    columns = []
    # noinspection PyProtectedMember
    model_conf = context['model']._meta.__dict__
    url_update = '%(app_label)s:%(model_name)s-modify' % model_conf
    url_delete = 'api:%(model_name)s-detail' % model_conf

    for td_conf in context['model'].html_table['td']:
        name = td_conf.get('dtt_name', td_conf['model_attr'])
        col = '{data: "' + td_conf['model_attr'] + '", name: "' + name + '"}'
        # override the anchor if its id  to update item
        if td_conf['model_attr'] == 'id' or td_conf.get('pk'):
            if 'update' in context['model'].html_table.get('controls', []):
                try:
                    edit_url = reverse(url_update, kwargs={'pk': 0}).replace('/0/', "/'+data+'/")
                except NoReverseMatch:
                    edit_url = reverse(
                        'srv:%(model_name)s-update' % model_conf, kwargs={'pk': 0}
                    ).replace('/0/', "/'+data+'/")
                col = '{data: "' + td_conf['model_attr'] + '", ' +\
                      """render: (data, type, row, meta)=>{return '<a class="btn-link" href=\"""" + \
                      edit_url + """\">'+data+'</a>'}}"""

        columns.append(col)

    # generate the anchor to delete item
    if 'delete' in context['model'].html_table.get('controls', []):
        if context['request'].user.has_perm('%(app_label)s.delete_%(model_name)s' % model_conf):
            delete_url = reverse(url_delete, kwargs={'pk': 0}).replace('/0/', "/'+data+'/")
            columns.append(
                '{data: "id", render: (data, type, row, meta)=>{ '
                f"""return '<a class="btn btn-danger delete-item" href="{delete_url}">"""
                """<i class="fas fa-trash-alt delete-item"></i></a>'}, searchable: false}"""
            )

    return mark_safe(str(',\n'.join(columns)))


@register.filter(name='checkbox_input', is_safe=True)
def checkbox_input(checked, **kwargs):
    _checked = 'checked' if checked else ''
    return mark_safe(f'<input type = "checkbox" {_checked} onclick="putObj(this);">')


@register.filter(name='text_input', is_safe=True)
def text_input(value, **kwargs):
    return mark_safe(f'<input type = "text" value="{value}" style="border: none;" size="10" oninput="putObj(this);">')


# noinspection PyProtectedMember
@register.simple_tag(takes_context=True)
def add_object_button(context):
    model_meta = context['model']._meta.__dict__
    try:
        url = reverse('%(app_label)s:%(model_name)s-add' % model_meta)
    except NoReverseMatch:
        url = reverse('srv:%(model_name)s-add' % model_meta)

    return mark_safe(f'<div class="row">'
                     f'<div class="col-sm-12 text-right">'
                     f'<div class="form-group">'
                     f'<a href="{url}" class="btn btn-success">Create {model_meta["verbose_name"]}</a>'
                     f'</div>'
                     f'</div>'
                     f'</div>')


@register.simple_tag(takes_context=True)
def table(context, object_list):
    return mark_safe(
        HtmlModelTable(object_list, context['request'].user).html
    )


html_table = {
    'attrs': [('class', 'table table-striped table-bordered')],
    'controls': ['delete', 'update', 'create', 'detail'],
}


class HtmlElement:
    """
    This is the base class for any html element tag
    it provides the html property that will return html representation of the object.
    If the innerHTML of the node is plain text its recommended to use escape=True example:

    In [5]: p = HtmlElement(
                    'p',
                    [('class', 'p-special-class'), ('style', 'display: flex;')],
                    '0 is not > than 1',
                    escape=True
                )
    In [6]: p.html
    Out[6]: '<p class="p-special-class"  style="display: flex;">0 is not &gt; than 1</p>'

    please notice the change of character ">" to &gt; so the browser understand that must show character ">" explicitly
    and not treat it as it was part of html code.

    however if innerHTML is another HtmlElement or HtmlList you leave escape=False as default is

    """
    def __init__(self, tag, attrs=None, inner_html=None, escape=False):
        self.tag = tag
        self.attrs = [] if not attrs else attrs
        self.inner_html = inner_html
        self.escape = escape

    def __str__(self):
        return f'<{self.__class__.__name__}: {self.tag}>'

    def __repr__(self):
        return self.__str__()

    def get_inner_html(self):
        if self.inner_html is None:
            return ''
        inner_html = self.inner_html.html if hasattr(self.inner_html, 'html') else self.inner_html
        if self.escape:
            return html.escape(inner_html)
        return inner_html

    @property
    def html(self):
        generated = {
            'tag': self.tag,
            'attrs': ' ' + ' '.join(['%s="%s"' % attr for attr in self.attrs]) if self.attrs else '',
            'inner_html': self.get_inner_html()
        }
        return '<%(tag)s%(attrs)s>%(inner_html)s</%(tag)s>' % generated


class HtmlList:
    def __init__(self, *args):
        self._elements = []
        if args:
            self._elements = args[0]

    def append(self, element):
        self._elements.append(element)

    @property
    def html(self):
        return ''.join([element.html for element in self._elements])


class HtmlModelTable(HtmlElement):
    """
    This class will create a html table for a given queryset
    contains thead and tbody
    """
    def __init__(self, queryset, user):
        self.attrs = []
        for k, v in queryset.model.html_table.items():
            setattr(self, k, v)

        super().__init__(
            'table',
            self.attrs,
            HtmlList([
                HtmlModelTHEAD(queryset, user),
                HtmlModelBODY(queryset, user),
            ])
        )


# noinspection PyUnresolvedReferences,PyProtectedMember
class HtmlModelTHEAD(HtmlElement):
    """
    This will create thead->tr->ths(s) if user has delete permissions over model it will ad an empty th
    to match tbody rows td(s) casuse tbody row will add a td to include delete button
    """
    def __init__(self, queryset, user):
        # get ths inner_html and create them
        val = [[v for k, v in i.items() if k == 'title'][0] for i in queryset.model.html_table['td']]
        ths = HtmlList([HtmlElement('th', [('scope', 'col')], i, escape=True) for i in val])

        if 'delete' in queryset.model.html_table.get('controls', []) \
                and user.has_perm('%(app_label)s.delete_%(model_name)s' % queryset.model._meta.__dict__):
            ths.append(HtmlElement('th', [], 'Actions'))
        # then append them to self
        super().__init__('thead', inner_html=ths)


class HtmlModelBODY(HtmlElement):
    """
    Its just a HtmlElement which has a tr htmlList
    """
    def __init__(self, queryset, user):
        super().__init__('tbody', inner_html=HtmlList([HtmlModelTR(obj, user) for obj in queryset]))


# noinspection PyUnresolvedReferences,PyProtectedMember
class HtmlModelTR(HtmlElement):
    """
    If user has delete permissions over model it will ad an additional th with delete button
    """
    def __init__(self, model_instance, user):
        self.attrs = []
        for k, v in model_instance.html_table.get('tr', {}).items():
            setattr(self, k, v)

        tds = HtmlList([HtmlModelTD(conf, model_instance) for conf in model_instance.html_table['td']])

        # append delete button
        if 'delete' in model_instance.html_table.get('controls', []) \
                and user.has_perm('%(app_label)s.delete_%(model_name)s' % model_instance._meta.__dict__):
            url = 'api:%(app_label)s-%(model_name)s-instance' % model_instance._meta.__dict__
            a_element = HtmlElement(
                'a',
                [
                    ('href', reverse(url, kwargs={'pk': model_instance.id})),
                    ('class', 'btn btn-danger delete-item')
                ],
                HtmlElement('i', [('class', 'fas fa-trash-alt')], '')
            )
            tds.append(HtmlElement('td', inner_html=a_element))

        super().__init__('tr', self.attrs, tds)


# noinspection PyUnresolvedReferences,PyProtectedMember
class HtmlModelTD(HtmlElement):
    def __init__(self, conf_data, obj):
        self.pk = False
        self.attrs = []
        self.parse = '{0}'
        self.default_if_none = None
        for k, v in conf_data.items():
            setattr(self, k, v)

        inner_html = self.parse_value(getattr(obj, self.model_attr))
        if self.model_attr == 'id':
            self.attrs.append(('scope', 'row'))
            try:
                url =reverse('%(app_label)s:%(model_name)s-update' % obj._meta.__dict__, kwargs={'pk': inner_html})
            except NoReverseMatch:
                url = reverse('srv:%(model_name)s-update' % obj._meta.__dict__, kwargs={'pk': inner_html})
            inner_html = HtmlElement(
                'a',
                [('href', url), ('class', 'btn-link')],
                inner_html
            )

        super().__init__(
            'td',
            self.attrs,
            inner_html,
            escape=(self.model_attr != 'id')
        )

    def parse_value(self, value):
        if self.default_if_none == value:
            return value
        if value is None and self.default_if_none is not None:
            return self.default_if_none

        return self.parse.format(value)
