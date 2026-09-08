from django.contrib import admin

from .models import (
    Property,
    PropertyImage,
    Favorite,
    Inquiry,
    Visit,
    Review,
    Notification,
    City,
    Category,
    Profile,
)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'city',
        'status',
        'agent',
    )

    search_fields = (
        'title',
        'description',
    )

    list_filter = (
        'status',
        'city',
        'category',
    )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'image',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'property',
    )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'property',
        'created_at',
        'status',
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'property',
        'visit_date',
        'status',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'property',
        'rating',
        'created_at',
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'message',
        'created_at',
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
