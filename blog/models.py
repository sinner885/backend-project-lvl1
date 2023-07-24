from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
# from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks.field_block import RichTextBlock, RawHTMLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.search import index


class BlogIndexPage(Page):
    subpage_types = ['BlogPage']
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class BlogPage(Page):
    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, help_text='суть статьи',
                             blank=True)
    body = StreamField([
        ('paragraph', RichTextBlock()),
        ('code', RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock())
    ], use_json_field=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = _('Blog post')
        verbose_name_plural = _('Blog posts')
