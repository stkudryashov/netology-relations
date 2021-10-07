from django.contrib import admin

from .models import Article
from .models import Tag
from .models import Relationship

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main = 0
        has_tag = False

        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                is_main += 1
            if form.cleaned_data.get('tag'):
                has_tag = True

        if is_main < 1 and has_tag:
            raise ValidationError('Укажите основной раздел')
        elif is_main > 1:
            raise ValidationError('Основным может быть только один раздел')

        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Relationship
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

