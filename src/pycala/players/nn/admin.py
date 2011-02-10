from django.contrib import admin

from pycala.players.nn import models

class NeuronAdmin(admin.ModelAdmin):
    
    list_display = ('probability','won','lost','draw','binary',)
    #search_fields = ('name','product_id',)
    #list_filter = ('added_on','is_published','categories',)
    #date_hierarchy = 'added_on'

admin.site.register(models.Neuron, NeuronAdmin)