from django.contrib.auth.models import User
from django.db import models
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly', max_length=100)
    highlighted = models.TextField()
    owner = models.ForeignKey(
        'auth.User', related_name='snippets', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

#
# Test
#


def init_data():
    admin = User.objects.get(username='admin')

    s1 = Snippet(owner=admin, title='foo', code='print(789)',
                 linenos=False, language='python', style='friendly')
    s1.save()

    s2 = Snippet(owner=admin, title='foo', code='foo="bar"',
                 linenos=False, language='python', style='friendly')
    s2.save()
    print('init data done')


def init_by_json_data():
    import json
    content = '{"title": "bar", "code": "print(\\"hello, python\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
    data = json.loads(content)
    admin = User.objects.get(username='admin')
    data['owner'] = admin
    s = Snippet(**data)
    s.save()

    print('count:', Snippet.objects.all().count())


def select_admin_snippet_data():
    admin = User.objects.get(username='admin')
    # use related_name "snippets" instead of "snippet_set"
    admin_snippets = admin.snippets.all()
    print('admin snippets:')
    for s in admin_snippets:
        print(s)
