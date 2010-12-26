from django.conf import settings
from django import forms
from django.db import models

from django.utils.safestring import mark_safe

class ForeignKeyAutocompleteInput(forms.widgets.Select):
    class Media:
        css = {
                'all': ('%s/css/jquery.autocomplete.css' % settings.MEDIA_URL,)
        }
        js = (
                '%s/js/jquery.js' % settings.MEDIA_URL,
                '%s/js/jquery.autocomplete.js' % settings.MEDIA_URL,
                '%s/js/autocomplete.popup.js ' % settings.MEDIA_URL
        )

    def text_field_value(self, value):
        key = self.rel.get_related_field().name
        obj = self.rel.to._default_manager.get(**{key: value})
        
        return unicode(obj)

    def __init__(self, rel, attrs=None):
        """
        rel - the relation for the foreign key.
        """
        self.rel = rel
        super(ForeignKeyAutocompleteInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        rendered = super(ForeignKeyAutocompleteInput, self).render(name, value, attrs)
        if value:
            text_field_value = self.text_field_value(value)
        else:
            text_field_value = u''
        return rendered + mark_safe(u'''
<input type="text" id="lookup_%(name)s" value="%(text_field_value)s" size="40" style="display: none;"/>
<script type="text/javascript">

$(document).ready(function(){
    // Javascript is required to show the autocomplete field and hide the select field.
    $("#id_%(name)s").hide();
    $("#lookup_%(name)s").show();

    function liFormat_%(name)s (row, i, num) {
            var result = row[0] ;
            return result;
    }
    
    var %(name)s_data = Array();
    var %(name)s_id_map = {};
    
    function load_autocomplete_data_from_select() {
        %(name)s_data = Array();
        %(name)s_id_map = {};
        $("#id_%(name)s option").each(function(d) {
            %(name)s_data.push($(this).html());
            %(name)s_id_map[$(this).html()] = $(this).val();
        })
        
        $("#lookup_%(name)s").autocomplete(%(name)s_data, {
            delay:10,
            minChars:1,
            matchSubset:1,
            autoFill:false,
            matchContains:1,
            cacheLength:10,
            selectFirst:true,
            formatItem:liFormat_%(name)s,
            maxItemsToShow:10
        }); 
    }
    
    load_autocomplete_data_from_select(); // Inital load
    
    // Changing the autocomplete field needs to change the hidden select field
    $("#lookup_%(name)s").change(function() {
        new_value = %(name)s_id_map[$(this).val()];
        if (new_value == undefined) {
            new_value = ""
        }
        $("#id_%(name)s").val(new_value); 
    })
    
    // It is possible to "change" the autocomplete text field and have the change
    // event not happen.  This double checks right before we submit.
    $("form").submit(function() {
        $("#lookup_%(name)s").change(); // Just to make sure
    })
    
    // When the add feature is used, it only knows how to change the select field
    // so the auto complete field needs to be updated too.
    $("#id_%(name)s").change(function () {
        $("#lookup_%(name)s").val($(this).find("option:selected").html());
        load_autocomplete_data_from_select(); // Could be a new value from an add
    })    
});
</script>
                ''') % {
                        'MEDIA_URL': settings.MEDIA_URL,
                        'model_name': self.rel.to._meta.module_name,
                        'app_label': self.rel.to._meta.app_label,
                        'text_field_value': text_field_value,
                        'name': name,
                        'value': value,
                }
