from django.contrib import admin

from memberManagement.models import Team, Membership, UserProfile

admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(Membership)
