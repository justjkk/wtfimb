from models import Route, RouteStage
from django.contrib.gis import admin
from django.core.urlresolvers import reverse

from reversion.admin import VersionAdmin
from autocomplete.admin import AutocompleteModelAdmin, AutocompleteTargetModelAdmin

class RouteStageInline(admin.TabularInline):
    model = RouteStage
    autocomplete_fields = ('stage')
    extra = 1
    ordering = ['stage__display_name']

class RouteAdmin(admin.OSMGeoAdmin,VersionAdmin, AutocompleteModelAdmin):
    ordering = ['city','display_name']
    autocomplete_fields = ('start','end')
    list_display = ('display_name', 'route_view_link', 'types', 'city',  'start', 'end', 'has_unmapped_stages')

    def has_unmapped_stages(self, obj):
        for s in obj.stages.all():
            if not s.location:
                return True
        return False
    has_unmapped_stages.boolean = True

    def route_view_link(self, obj):
        return "<a href='%s'>View Link</a>" % reverse('show-route', args=[obj.city, obj.slug])

    route_view_link.allow_tags = True
    route_view_link.short_description = "Link to Site"

    inlines = (RouteStageInline, )

    prepopulated_fields = {"slug": ("display_name",)}

admin.site.register(Route, RouteAdmin)
