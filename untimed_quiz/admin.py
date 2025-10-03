
from django.contrib import admin
from .models import UntimedCategory, UntimedQuestion, UntimedUserResponse

# Register the UntimedCategory model
@admin.register(UntimedCategory)
class UntimedCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# Register the UntimedQuestion model
@admin.register(UntimedQuestion)
class UntimedQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "text")
    search_fields = ("text",)
    list_filter = ("category",)

# Register the UntimedUserResponse model
@admin.register(UntimedUserResponse)
class UntimedUserResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "is_correct")
    search_fields = ("user__username", "question__text")
    list_filter = ("is_correct",)
