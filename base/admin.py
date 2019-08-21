from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from base.models import Rubric, Market, Product


class MarketAdmin(admin.ModelAdmin):

    @staff_member_required
    def my_view(self, request):
        return render(request, 'base/done.html', {})


admin.site.register(Market, MarketAdmin)
admin.site.register(Rubric)
admin.site.register(Product)
