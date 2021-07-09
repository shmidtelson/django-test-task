from django.contrib import admin

from auction.models import Item, Bet, Lot, Profile


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)


class LotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lot, LotAdmin)


class BetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bet, BetAdmin)


class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
