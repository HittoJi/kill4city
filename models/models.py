# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
from datetime import datetime, timedelta
import logging
import math
from openerp.exceptions import ValidationError

# Git 29 dic

class zone(models.Model):
    _name = 'kill4city.zone'
    _description = 'kill4city.zone'

    def _generate_town_name(self):
        towns = ["Oscoz","Torrelara","Coscullano","Cicera","Haedillo","Eustaquios","Navarredondilla","Elda","Garayolza","Marne","Santiorjo","Delfiá","Malá","Noia","Puertas","Sardas","Felechosas","Bujursot","Betolaza","Batiao","Berzosa","Rigueira","Guaso","Bode","Logrosa","Vilamitjana","Cogela","Royo","Solmayor","Daneiro","Fornes","Medal","Infesta","Ludrio","Torregorda","Cereijido","Sanjurjo","Corres","Espasantes","Igea","Pierres","Carabias","Concha","Torleque","Viella","Arro","Cegama","Jubia","Torquiendo","Loja"]
        return random.choice(towns)

    def _generate_zone_level(salf):
        # Futura mejora => Mirar la cantidad de zonas que tiene una ciudad 
                            # para generar minimo un 3% de zonas con un nivel 1 y
                            # un 5% de zonas al nivel 100;
                            # => Mirar el nivel del jugador para crear zonas apartit de su nuvel
                            
        return random.randint(0,100)
    


    level = fields.Integer(default=_generate_zone_level)
    
    # def _generate_live_heal(level):
    #     # Revisar
    #     return 202 * 2


    name = fields.Char(default=_generate_town_name)
    conquest = fields.Float()
    # conquest = fields.Float(compute='_calculate_conquer_porcenta_zone')
    status = fields.Char(default="Invaded")
    # status = fields.Boolean()
    
    # @api.depends('status')
    # def _calculate_conquer_porcenta_zone(self):
    #     for zone in self:
    #         if zone.status:
    #             zone.conquest = 70
                
    def new_name(self):
        towns = ["Oscoz","Torrelara","Coscullano","Cicera","Haedillo","Eustaquios","Navarredondilla","Elda","Garayolza","Marne","Santiorjo","Delfiá","Malá","Noia","Puertas","Sardas","Felechosas","Bujursot","Betolaza","Batiao","Berzosa","Rigueira","Guaso","Bode","Logrosa","Vilamitjana","Cogela","Royo","Solmayor","Daneiro","Fornes","Medal","Infesta","Ludrio","Torregorda","Cereijido","Sanjurjo","Corres","Espasantes","Igea","Pierres","Carabias","Concha","Torleque","Viella","Arro","Cegama","Jubia","Torquiendo","Loja"]
        for zone in self:
            zone.name = random.choice(towns);

    @api.depends('level')
    def _calculate_food_zone(self):
        for zone in self:
            zone.food = zone.level*2
            
    food = fields.Integer(default=404)
    # live_heal = fields.Integer(default=_generate_live_heal)
    # liveHeal = fields.Integer(default=_generate_live_heal,readonly=True)

    city = fields.Many2one("kill4city.city", ondelete='cascade')        
    
    @api.model
    def create(self,values):
        record = super(zone, self).create(values)
        if record.food == 404:
          record.write({'food': record.level*2})
        return record

    @api.onchange('name')
    def _onchange_name(self):
        print("name change")
    
    @api.constrains('level')
    def _check_something(self):
        for record in self:
            if record.level > 100:
                raise ValidationError("The zone level must be between 1 and 100: %s" % record.level)

class city(models.Model):
    _name = 'kill4city.city'
    _description = 'kill4city.city'

    def _generate_city_name(self):
        citys = ["Willesden","Chesterfield","Hewe","Orilon","Hartlepool","Dragontail","Whitebridge","Beckton","Achnasheen","Foolshope","Mirstone","Aynor","Nearon","Drumnadrochit","Oldham","Hirane","Haedleigh","Calcherth","Dundee","Auchenshuggle","Clare View Point","Dumbarton","Haling Cove","Damerel","Bredon","Axminster","Cesterfield","Todmorden","Blencalgo","Worcester"]
        return random.choice(citys)
    def _generate_zones(salf):
        return random.randint(2,5)


    name = fields.Char(default=_generate_city_name)
    zones = fields.Integer(default=_generate_zones)

    zone = fields.One2many("kill4city.zone","city")
    max_players = fields.Integer(compute="_get_zones")  #get quantity of zones and divide by 2 to set the total amout of player can acces to the city
    players_in = fields.One2many("kill4city.player","in_city")

    
    @api.model
    def create(self, vals_list):
        new_object_city = super(city, self).create(vals_list)
        for i in range(new_object_city.zones):
            self.env["kill4city.zone"].create({"city":new_object_city.id})
        return new_object_city
    
    @api.depends('zones')
    def _get_zones(self):
        for city in self:
            city.max_players = city.zones/2


class training(models.Model):
    _name = 'kill4city.training'
    _description = 'kill4city.training'

    player = fields.Many2one("kill4city.player", required = True, ondelete='cascade')
    training_type = fields.Selection([('brain', 'Brain'),('power','Power')] , required = True)
    start_time = fields.Datetime(readonly=True)
    end_time = fields.Datetime(readonly=True)
    training_in_process = fields.Boolean(default=False)
    training_bar = fields.Float(default=0)


    @api.model
    def create(self,values):
        record = super(training, self).create(values)
        record.start_time = fields.Datetime.to_string(datetime.now())
        record.end_time = fields.Datetime.to_string(fields.Datetime.from_string(fields.datetime.now()) + timedelta(hours=168))
        record.training_in_process = True
        return record
    
    @api.model
    def training_process(self):
        allTraining = self.search([('training_in_process','=',True),('training_bar','>',100)])
        for training in allTraining:
            # Calculate % to increment
            if training.training_type == 'brain':
                next_reword = ((training.player.smart*2)/100) / 168
            if training.training_type == 'power':
                next_reword = ((training.player.power*2)/100) / 168
                training.player.power += next_reword
                training.training_bar += (100 * next_reword) / 2
                training.player.life -= next_reword * 3

            if training.start_time >= training.end_time:
                training.training_in_process = False
                print("Training has end")

            print("Cron tringin done")

                

    # def increment(self):
    #     allTraining = self.search([('training_in_process','=',True),('training_bar','<',100)])
    #     for training in allTraining:
    #         # Calculate % to increment
    #         if training.training_type == 'brain':
    #             next_reword = ((training.player.smart*2)/100) / 168
    #         if training.training_type == 'power':
    #             next_reword = ((training.player.power*2)/100) / 168
    #         training.player.power += next_reword
    #         training.training_bar += (100 * next_reword) / 2
    #         training.player.life -= next_reword * 3

    #         # training.start_time += timedelta(hours=50)

    #         if training.start_time >= training.end_time:
    #             training.training_in_process = False
    #             print("Son iguales")
    #         print("Cron tringin done")
    #         print(training.player.life)
    #         print(next_reword)

            
                



class player(models.Model):
    _name = 'kill4city.player'
    _description = 'kill4city.player'

    def _generate_player_name(self):
        ranName = ["Isabel Saldaña","Mariam Contador","Noemi Monte","Vanessa Villalobos","Nerea Racionero","Uxia Barbero","Fatima Marinero","Nora Balderas","Ana Isabel Sallent","Ainoa Carpentier","Angel Hernández","Iago Jurado","Jose Maria Valderas","Alonso Panadero","Matias Villalba","Isaac Alcaide","Kevin Rabellino","Francisco Padrón","Jordi Val","Salvador Balderas","Gerard Morterero","Miguel Mallén","Alonso del Valle","Pol Domínguez","Jon Ferrero","Ramon Fuster o Fusté","Oliver Hernández","Sergi Bielsa","Rodrigo Enríquez","Pau Ascaso","Mar Valverde","Gabriela Santolaria","Patricia Ordóñez","Judith Siurana","Judit Villalobos","Mireya Pajarero","Clara Racionero","Carmen Maria Molinero","Zaira Martín","Neus Peña"]
        return random.choice(ranName)

    def _calculate_random_num(salf):
        return random.randint(3,30)

    name = fields.Char(default=_generate_player_name)
    level = fields.Integer(default=1)
    life = fields.Float(default=100)
    smart = fields.Float(default=_calculate_random_num)
    power = fields.Float(default=_calculate_random_num)

    weapon = fields.Many2one("kill4city.weapon")
    training = fields.Many2one("kill4city.training")
    in_city = fields.Many2one("kill4city.city",ondelete="set null")
    in_battle = fields.Boolean(default=False)


class weapon(models.Model):
    _name = 'kill4city.weapon'
    _description = 'kill4city.weapon'

    name = fields.Char()
    damage = fields.Integer()
    photo = fields.Image(max_width=100, max_height=100)
    use_by = fields.One2many("kill4city.player","weapon")

class conquer(models.Model):
    _name = 'kill4city.conquer'
    _description = 'kill4city.conquer'

    zone = fields.Many2one("kill4city.zone", required = True, ondelete='cascade')
    player = fields.Many2one("kill4city.player", required = True, ondelete='cascade')
    start_time = fields.Datetime(readonly=True)
    end_time = fields.Datetime(readonly=True)
    # end_time = fields.Datetime(compute='_calculate_end_time')
    percentage_conquers = fields.Float(default=0)
    player_life = fields.Integer(default=0)
    in_battle = fields.Boolean()


    @api.depends('start_time','player','zone')
    def _calculate_end_time(self):
        for conq in self:
            if p != 0 and z != 0:
                conq.player_life = conq.player.life
            print("You just set the time")

    @api.model
    def create(self,values):
        record = super(conquer, self).create(values)
        if record.start_time != "":    
            record.start_time = fields.Datetime.to_string(datetime.now())
            # Calculate end time
            p = record.player.level
            w = record.player.weapon.damage
            z = record.zone.level
            time_end_calculate = math.log(z* (p*w),2)
            record.end_time = fields.Datetime.to_string(fields.Datetime.from_string(fields.datetime.now()) + timedelta(hours=time_end_calculate))
            record.player_life = record.player.life
            record.in_battle = True

        return record



    @api.model
    def update_conquer(self):
        allConquer = self.search([('in_battle','=',True)])
        # for c in allConquer:
        #     diff = c.end_time - c.start_time
        #     days, seconds = diff.days, diff.seconds
        #     hours = days * 24 + seconds 
        #     minutes = (seconds % 3600)
        #     seconds = seconds % 60
        #     tmpone = hours + (minutes / 60 + ((seconds / 60)/60))

        #     # then get the diference between end and now time 
        #     diff = c.end_time - datetime.now()
        #     days, seconds = diff.days, diff.seconds
        #     hours = days * 24 + seconds 
        #     minutes = (seconds % 3600)
        #     seconds = seconds % 60
        #     tmptwo = hours + (minutes / 60 + ((seconds / 60)/60))

        #     # calculate the porcenta between the two times
        #     result = (tmptwo * 100 /(tmpone)) - 100

        #     # Set the porcenta for procces bar 
        #     c.zone.conquest = abs(result)
        #     c.percentage_conquers = abs(result)

        #     # player_life = c.player.life Aquiiiiiiiiiiii no vaaa buscate la vida
        #     # Calculate player life damage
        #     c.player.life -= c.percentage_conquers;
        #     if c.zone.conquest >= 100:
        #         c.zone.status = "released"
        #     print("===CRON===")
        #     c.in_battle = False
        #     print(c.in_battle)

    def increment(self):
        allConquer = self.search([('in_battle','=',True)])
        for c in allConquer:
            diff = c.end_time - c.start_time
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds 
            minutes = (seconds % 3600)
            seconds = seconds % 60
            tmpone = hours + (minutes / 60 + ((seconds / 60)/60))

            # get the diference between start and end time
            diff = c.end_time - datetime.now()
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds 
            minutes = (seconds % 3600)
            seconds = seconds % 60
            tmptwo = hours + (minutes / 60 + ((seconds / 60)/60))

            # calculate the porcenta between the two times
            result = (tmptwo * 100 /(tmpone)) - 100

            # Set the porcenta for procces bar 
            c.zone.conquest = abs(result)
            c.percentage_conquers = abs(result)

            # Calculate player life damage (danger = Zone - player life)
            

            c.player.life -= c.zone.level - c.player.level
            c.player_life = c.player.life

            # Calculate zone damage by the player

            # if the player is dead
            if c.player.life <= 0:
                c.player.life = 0
                c.player_life = 0
                c.in_battle = False


    

            
                
    #  for conq in self:
    #         p = conq.player.level
    #         w = conq.player.weapon.damage
    #         z = conq.zone.level
    #         # if conq.record.start_time == "":    
    #         #     conq.start_time = fields.Datetime.to_string(datetime.now())
    #             # fix the time start*--------------------
    #         if p != 0 and z != 0:
    #             time_end_calculate = math.log(z* (p*w),2)
    #             conq.end_time = fields.Datetime.to_string(fields.Datetime.from_string(fields.datetime.now()) + timedelta(hours=time_end_calculate))
    #             # conq.start_time = fields.Datetime.to_string(datetime.now())
    #             conq.player_life = conq.player.life
    #             conq.player.in_battle = True
    #             conq.in_battle = True
    #             print("You just set the time")
    #         else:
    #             conq.end_time = fields.Datetime.to_string(datetime.now())
    #             # conq.zone.status = False