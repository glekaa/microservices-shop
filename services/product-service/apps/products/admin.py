from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<strong>{}</strong>', count)

    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_status', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at', 'is_in_stock')
    list_per_page = 25

    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'is_in_stock')
        }),
        ('Media', {
            'fields': ('image_url',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            color = 'red'
            status = 'Out of Stock'
        elif obj.stock_quantity < 10:
            color = 'orange'
            status = 'Low Stock'
        else:
            color = 'green'
            status = 'In Stock'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )

    stock_status.short_description = 'Stock Status'

    actions = ['mark_as_active', 'mark_as_inactive', 'replenish_stock']

    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} product(s) marked as active.')

    mark_as_active.short_description = 'Mark selected products as active'

    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} product(s) marked as inactive.')

    mark_as_inactive.short_description = 'Mark selected products as inactive'

    def replenish_stock(self, request, queryset):
        for product in queryset:
            product.stock_quantity += 100
            product.save()
        self.message_user(request, f'{queryset.count()} product(s) restocked with 100 units each.')

    replenish_stock.short_description = 'Replenish stock (+100 units)'