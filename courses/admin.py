from django.contrib import admin

from .models import Course, CoursePart


def some_admin_action(modeladmin, request, queryset):
    print(queryset)


class CoursePartInline(admin.StackedInline):
    model = CoursePart
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = (CoursePartInline,)
    actions = (some_admin_action,)
    # fields = ('title', 'description', 'deleted_at')

    fieldsets = (
        ("Major fileds", {"fields": ("description", "title")}),
        ("Minor fileds", {"fields": ("deleted_at", "created_by")}),
    )

    list_display = ("id", "title", "description", "part_count")

    def part_count(self, obj):
        return obj.parts.count()

    part_count.short_description = "Couse Parts Amount"

    list_filter = ("title", "created_by")

    search_fields = ("title", "description")

    list_editable = ("title",)

    ordering = ("-id",)


# Register your models here.
admin.site.register(Course, CourseAdmin)
