from django.core.management.base import BaseCommand, CommandError
from django.db import models
from scan.models import Competition, Match, Team, Player, Lineup

import requests
import json
import time

urlteams = 'http://api.football-data.org/v2/competitions/2014/matches'


class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(urlteams, headers={'X-Auth-Token':'dfec1fbedad7421abdad5eda2372b4c2'})
        matches = json.loads(r.text)['matches']
        partidos = []
        for i in matches:
            try:
                p = i['id']
                partidos.append(p)
            except:
                pass    
        for i in partidos:
            try:
                url = 'http://api.football-data.org/v2/matches/' + str(i)
                print('BUSCANDO EL PARTIDO CON URL %s' % url)
                r = requests.get(url, headers={'X-Auth-Token':'dfec1fbedad7421abdad5eda2372b4c2'})
                local = json.loads(r.text)['match']['homeTeam']['name']
                visitor = json.loads(r.text)['match']['awayTeam']['name']
                print('EL EQUIPO LOCAL ES %s' % local)
                print('EL EQUIPO VISITANTE ES %s' % visitor)
                localteam = Team.objects.get(name=local)
                visitorteam = Team.objects.get(name=visitor)
                Match.objects.create(matchid=i, local=localteam, visitor=visitorteam)
                print('CREADO EL PARTIDO CON LOS EQUIPOS %s' % (local,visitorteam))
                sleep(11)
            except Exception as e:
                print(e)
                pass
            
        print('finito')    
    
    
        
                
        
