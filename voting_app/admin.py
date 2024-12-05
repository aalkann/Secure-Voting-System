from django.contrib import admin
from .models import Election, Candidate, Vote

admin.site.register(Election)
admin.site.register(Candidate)


class VoteAdmin(admin.ModelAdmin):
    exclude = ('cipher_text','exponent',) 
    readonly_fields = ('candidate',)

admin.site.register(Vote, VoteAdmin)