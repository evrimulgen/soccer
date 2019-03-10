from django.core.management.base import BaseCommand, CommandError
from django.db import models
from scan.models import Competition, Match, Team, Player, Lineup

import requests
import json
import time

urlmatches = 'http://api.football-data.org/v2/competitions/2014/matches'


class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(urlmatches, headers={'X-Auth-Token':'dfec1fbedad7421abdad5eda2372b4c2'})
        matches = json.loads(r.text)['matches']
        time.sleep(3)
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
                print('PROCEDIENDO A AÑADIR ALINEACIONES')
                time.sleep(2)
                l = json.loads(r.text)['match']['homeTeam']['name']
                v = json.loads(r.text)['match']['awayTeam']['name']
                print('EL EQUIPO LOCAL ES %s' % l)
                print('EL EQUIPO VISITANTE ES %s' % v)
                
                casa = Team.objects.get(name=l)
                fuera = Team.objects.get(name=v)
                local_lineup = []
                visitor_lineup = []
                homelineup = json.loads(r.text)['match']['homeTeam']['lineup']
                awaylineup =  json.loads(r.text)['match']['awayTeam']['lineup']
                for h in homelineup:
                    local_lineup.append(h['id'])
                for v in awaylineup:
                    visitor_lineup.append(v['id'])
                    
                print('LA ALINEACIÓN DEL LOCAL ES %s' % local_lineup)
                print('LA ALINEACIÓN DEL VISITANTE ES %s' % visitor_lineup)
                
                localplayers = []
                visitorplayers = []
                codigolocal = ''
                codigovisitante = ''
                
                for i in local_lineup:
                    try:
                        player = Player.objects.get(name=str(i))
                    except:
                        Player.objects.create(name = str(i), team=casa)
                        print('Creado el jugador %s' % i)
                        player = Player.objects.get(name=str(i))                        
                    inicial = str(i)[:1]
                    codigolocal += inicial
                    localplayers.append(player)
                print('EL NOMBRE DE LA ALINEACION LOCAL ES %s' % codigolocal)  
                
                for i in visitor_lineup:
                    try:
                        player = Player.objects.get(name=str(i))
                    except:    
                        Player.objects.create(name = str(i), team=fuera)
                        player = Player.objects.get(name=str(i))
                        print('Creado el jugador %s' % i)
                    inicial = str(i)[:1]
                    codigovisitante += inicial
                    visitorplayers.append(player)  
                print('EL NOMBRE DE LA ALINEACION VISITANTE ES %s' % codigovisitante)    
                
                alocal = casa.lineup_set.all()
                codigoslocal = []
                
                if len(alocal) == 0:
                    Lineup.objects.create(lineupid=codigolocal, team=casa)
                    Lineup.objects.update(lineupid=codigolocal, team=casa, players=localplayers)
                    print('PRIMERA ALINEACION CREADA CON ID %s' % codigolocal)
                else:
                    for i in alocal:
                        codigoslocal.append(i.linupid)
                    if lineupid in codigoslocal:
                        pass
                    else:  
                        Lineup.objects.create(lineupid=codigolocal, team=casa)
                        Lineup.objects.update(lineupid=codigolocal, team=casa, players=localplayers)
                        print('CREATED LINEUP %s' % codigolocal)
                         
                avisitante = fuera.lineup_set.all()
                codigosvisitante = []
                
                if len(avisitante) == 0:
                    Lineup.objects.create(lineupid=codigovisitante, team=fuera)
                    Lineup.objects.update(lineupid=codigovisitante, team=fuera, players=visitorplayers)
                    print('PRIMERA ALINEACION CREADA CON ID %s' % codigolocal)
                else:
                    for i in avisitante:
                        codigosvisitante.append(lineupid)
                    if lineupid in codigoslocal:
                        pass
                    else:  
                        Lineup.objects.create(lineupid=codigovisitante, team=fuera)
                        Lineup.objects.create(lineupid=codigovisitante, team=fuera, players=visitorplayers)
                        print('CREATED LINEUP %s' % codigovisitante)
    
            except Exception as e:
                print(e)
                pass
    print('process finished')        
