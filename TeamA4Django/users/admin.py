from django.contrib import admin
from .models import UserProfile, CreditCard, Movie, Customer, Bookings, Showtimes
from .models import Admin, Promotions, Show, TicketPrices, Showroom, Ticket
from .models import Show
from .forms import ShowAdminForm

admin.site.register(UserProfile)
admin.site.register(CreditCard)
admin.site.register(Movie)
admin.site.register(Customer)
admin.site.register(Bookings)
admin.site.register(Showtimes)
admin.site.register(Admin)
# admin.site.register(Promotions)
# admin.site.register(Show)
admin.site.register(Ticket)
admin.site.register(TicketPrices)
admin.site.register(Showroom)



class ShowAdmin(admin.ModelAdmin):
    form = ShowAdminForm

admin.site.register(Show, ShowAdmin)

# Register your models here.
class PromotionsAdmin(admin.ModelAdmin):
    # Fields to display in the admin interface
    list_display = ('code', 'percentage', 'start_date', 'end_date', 'show', 'is_available')

    # Make all fields read-only
    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, i.e., we are editing an existing object
            return self.readonly_fields + ('code', 'percentage', 'start_date', 'end_date', 'show', 'is_available')
        return self.readonly_fields

# Register the Promotions model with the custom admin class
admin.site.register(Promotions, PromotionsAdmin)