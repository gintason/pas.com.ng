from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import PasswordReset
import openpyxl
from django.http import HttpResponse

User = get_user_model()


@admin.action(description="Export selected users to Excel")
def export_users_to_excel(modeladmin, request, queryset):
    # Create a new Excel workbook and sheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Users"

    # Define headers
    headers = ["ID", "Username", "Email", "First Name", "Last Name", "Is Staff", "Date Joined"]
    worksheet.append(headers)

    # Add user data
    for user in queryset:
        worksheet.append([
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.is_staff,
            user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    # Prepare response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename=users_export.xlsx'
    workbook.save(response)
    return response


# ✅ Unregister the default User admin first
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Ignore if it was not registered before


# ✅ Register custom User admin with export action
@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    actions = [export_users_to_excel]


# Register your custom models
admin.site.register(PasswordReset)
