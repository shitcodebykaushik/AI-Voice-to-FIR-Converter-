from django.contrib import admin
from .models import Audio, FIR


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'created_at')
    search_fields = ('id',)
    ordering = ('-created_at',)


@admin.register(FIR)
class FIRAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'created_at')
    search_fields = ('case_id',)
    ordering = ('-created_at',)
    readonly_fields = ('case_id', 'fir_pdf')
