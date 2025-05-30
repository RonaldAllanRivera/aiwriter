# generator/admin.py
from django.contrib import admin
from .models import GenerationLog, TrialSessionLog, PurchaseLog
from django.contrib.admin import SimpleListFilter


admin.site.register(GenerationLog)

class AbuseScoreFilter(SimpleListFilter):
    title = 'Abuse Score'
    parameter_name = 'abuse_flagged'

    def lookups(self, request, model_admin):
        return (
            ('flagged', 'Abuse Score ≥ 1'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'flagged':
            return queryset.filter(abuse_score__gte=1)
        return queryset


@admin.register(TrialSessionLog)
class TrialSessionLogAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address', 'trial_uses', 'abuse_score', 'is_incognito',
        'linked_user', 'registered', 'created_at', 'last_used_at'
    )
    list_filter = ['is_incognito', 'registered', 'created_at', AbuseScoreFilter]
    search_fields = ['ip_address', 'user_agent']
    ordering = ['-created_at']

    def short_user_agent(self, obj):
        return obj.user_agent[:60] + "..." if len(obj.user_agent) > 60 else obj.user_agent
    short_user_agent.short_description = "User Agent"



@admin.register(PurchaseLog)
class PurchaseLogAdmin(admin.ModelAdmin):
    list_display = ("user", "credits", "amount", "status", "created_at")
    search_fields = ("user__email", "stripe_session_id")
    list_filter = ("status", "created_at")
