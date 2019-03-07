from scan.models import Competition, Match, Team, Player, Lineup
from django.contrib import admin


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)

admin.site.register(Competition, CompetitionAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['matchday']
    list_filter = ('matchday',)
    
admin.site.register(Match, MatchAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'coach']
    list_filter = ('name',)

admin.site.register(Team, TeamAdmin)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'age']
    list_filter = ('name',)

admin.site.register(Player, PlayerAdmin)

class LineupAdmin(admin.ModelAdmin):
    list_display = ['team', 'timeplayed', 'goalsfavor', 'goalscounter']
    
admin.site.register(Lineup, LineupAdmin)
