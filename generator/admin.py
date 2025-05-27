from django.contrib import admin
from .models import GenerationLog
from .models import TrialAccessLog

admin.site.register(GenerationLog)
admin.site.register(TrialAccessLog)
