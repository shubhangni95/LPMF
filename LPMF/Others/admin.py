from django.contrib import admin
from . import models
from .models import MediaImagesAndVideo, MediaAndPresskit
# Register your models here.


class MediaImagesAndVideoAdmin(admin.StackedInline):
    model = MediaImagesAndVideo


@admin.register(MediaAndPresskit)
class MediaAndPresskitAdmin(admin.ModelAdmin):
    inlines = [MediaImagesAndVideoAdmin]

    class Meta:
        model = MediaAndPresskit


@admin.register(MediaImagesAndVideo)
class MediaImagesAndVideoAdmin(admin.ModelAdmin):
    pass


class ToolsDataAdmin(admin.ModelAdmin):
    list_display = ('tool_heading_name', 'tool_discription', 'tool_category', 'tool_version_number', 'tool_file_size',
                    'tool_support_document_link', 'tool_uploaded_date', 'tool_last_updated_date', 'tool_download_counter')
    search_fields = ['tool_heading_name', 'tool_category']
    ordering = ['tool_uploaded_date']
    list_filter = ['tool_category', 'tool_heading_name']




# Register Articles Models


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('article_heading_name', 'article_created_date',
                    'article_last_updated_date', 'article_author_name', 'article_published_status', 'article_published_date')


admin.site.register(models.Articles, ArticlesAdmin)
admin.site.register(models.Category)
admin.site.register(models.ToolsData, ToolsDataAdmin)
admin.site.register(models.UpcomingNewsAndEvents)
admin.site.register(models.Services)
admin.site.register(models.Feedback)
admin.site.register(models.Faq)
admin.site.register(models.UserRegistration)
admin.site.register(models.Country)
admin.site.register(models.States)
admin.site.register(models.City)
# admin.site.register(models.UserProfile)
admin.site.register(models.Blogs)
# admin.site.register(models.MediaAndPresskit)
# admin.site.register(models.MediaImagesAndVideo)
admin.site.register(models.Bookmarks)
