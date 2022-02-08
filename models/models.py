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
                            
        return random.randint(1,100)
    


    level = fields.Integer(default=_generate_zone_level)

    defense = fields.Integer(default=0)
    danger = fields.Integer(default=0)


    
    def _calculate_defense(salf):
        calculate_defense = 0
        for zone in salf:
            min_num = zone.level - 5
            max_num = zone.level + 5
            calculate_defense = random.randint(min_num, max_num)
            # if calculate_danger > 100:
            # calculate_danger = 100
            # if calculate_danger < 3:
            # calculate_danger = 5
        return abs(calculate_defense)

    def _calculate_danger(salf):
        calculate_danger = 0
        for zone in salf:
            min_num = zone.defense - 5
            max_num = zone.food + 5
            calculate_danger = random.randint(min_num, max_num)
            # if calculate_danger > 100:
            # calculate_danger = 100
            # if calculate_danger < 3:
            # calculate_danger = 5
        return abs(calculate_danger)


    name = fields.Char(default=_generate_town_name)
    conquest = fields.Float()
    status = fields.Char(default="Invaded")
                
    def new_name(self):
        towns = ["Oscoz","Torrelara","Coscullano","Cicera","Haedillo","Eustaquios","Navarredondilla","Elda","Garayolza","Marne","Santiorjo","Delfiá","Malá","Noia","Puertas","Sardas","Felechosas","Bujursot","Betolaza","Batiao","Berzosa","Rigueira","Guaso","Bode","Logrosa","Vilamitjana","Cogela","Royo","Solmayor","Daneiro","Fornes","Medal","Infesta","Ludrio","Torregorda","Cereijido","Sanjurjo","Corres","Espasantes","Igea","Pierres","Carabias","Concha","Torleque","Viella","Arro","Cegama","Jubia","Torquiendo","Loja"]
        for zone in self:
            zone.name = random.choice(towns);

    @api.depends('level')
    def _calculate_food_zone(self):
        for zone in self:
            zone.food = zone.level*2
            
    food = fields.Integer(default=404)

    city = fields.Many2one("kill4city.city", ondelete='cascade')        
    
    @api.model
    def create(self,values):
        record = super(zone, self).create(values)
        if record.food == 404:
            record.write({'food': record.level*2})
            record.defense = record._calculate_defense()
            record.danger = record._calculate_danger()
        
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
        return random.randint(2,50)


    name = fields.Char(default=_generate_city_name)
    zones = fields.Integer(default=_generate_zones)

    zone = fields.One2many("kill4city.zone","city")
    max_players = fields.Integer(compute="_get_zones")  #get quantity of zones and divide by 2 to set the total amout of player can acces to the city
    players_in = fields.One2many("res.partner","in_city")

    
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

    player = fields.Many2one("res.partner", required = True, ondelete='cascade')
    training_type = fields.Selection([('brain', 'Brain'),('power','Power')] , required = True)
    start_time = fields.Datetime(readonly=True)
    end_time = fields.Datetime(readonly=True)
    training_in_process = fields.Boolean(default=False)
    training_bar = fields.Float(default=0)
    start_power = fields.Float(default=0)
    start_smart = fields.Float(default=0)
    start_life = fields.Float(default=0)
    total_reword = fields.Float(default=0)

    @api.model
    def create(self,values):
        record = super(training, self).create(values)
        record.start_time = fields.Datetime.to_string(datetime.now())
        record.end_time = fields.Datetime.to_string(fields.Datetime.from_string(fields.datetime.now()) + timedelta(hours=168))
        # record.end_time = fields.Datetime.to_string(fields.Datetime.from_string(fields.datetime.now()) + timedelta(hours=0.05))
        record.start_power = record.player.power
        record.start_smart = record.player.smart
        record.start_life = record.player.life
        record.training_in_process = True
        record.player.occupied = True
        return record
    
    @api.model
    def training_process(self):
        allTraining = self.search([('training_in_process','=',True)])
        for training in allTraining:
            if datetime.now() >= training.end_time:
                training.training_in_process = False
                training.player.occupied = False
                training.training_bar = 100
                if training.training_type == 'brain':
                    training.player.smart = training.start_smart + training.total_reword
                if training.training_type == 'power':
                    training.player.power = training.start_power + training.total_reword
                print("Training has end")

            else:
                # # Calculate % to increment
                time_elapsed = abs((training.start_time - training.end_time).total_seconds() / 60)
                current_time = abs((datetime.now() - training.end_time).total_seconds() / 60)
                progress = 100 - ((100*current_time)/time_elapsed)
                training.training_bar = progress

                if training.training_type == 'brain':
                    progress_estimate = 10 - (math.log(training.player.level * training.start_smart,3))
                    total_reword = (training.start_smart * progress_estimate) / 100
                    current_reword = (total_reword * progress) / 100
                    training.player.smart = training.start_smart + current_reword
                    training.player.life = training.start_life - (math.log(training.player.level * training.start_smart,2))
                    training.total_reword = total_reword

                if training.training_type == 'power':
                    progress_estimate = 10 - (math.log(training.player.level * training.start_power,3))
                    total_reword = (training.start_power * progress_estimate) / 100
                    current_reword = (total_reword * progress) / 100
                    training.player.power = training.start_power + current_reword
                    training.player.life = training.start_life - (math.log(training.player.level * training.start_power,2))
                    training.total_reword = total_reword
            print("Cron tringin done")
            print(training.total_reword)


    def cancel_training(self):
        for training in self:
            training.training_in_process = False
            training.player.occupied = False
            print(training.total_reword)
        action = self.env.ref('kill4city.action_training_window').read()[0]
        return action
        # return {'type': 'ir.actions.client','tag': 'reload',}

            
                



class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    # _description = 'res.partner'

    def _generate_player_name(self):
        ranName = ["Isabel Saldaña","Mariam Contador","Noemi Monte","Vanessa Villalobos","Nerea Racionero","Uxia Barbero","Fatima Marinero","Nora Balderas","Ana Isabel Sallent","Ainoa Carpentier","Angel Hernández","Iago Jurado","Jose Maria Valderas","Alonso Panadero","Matias Villalba","Isaac Alcaide","Kevin Rabellino","Francisco Padrón","Jordi Val","Salvador Balderas","Gerard Morterero","Miguel Mallén","Alonso del Valle","Pol Domínguez","Jon Ferrero","Ramon Fuster o Fusté","Oliver Hernández","Sergi Bielsa","Rodrigo Enríquez","Pau Ascaso","Mar Valverde","Gabriela Santolaria","Patricia Ordóñez","Judith Siurana","Judit Villalobos","Mireya Pajarero","Clara Racionero","Carmen Maria Molinero","Zaira Martín","Neus Peña"]
        return random.choice(ranName)

    def _calculate_random_num(salf):
        return random.randint(3,30)

    # name = fields.Char(default=_generate_player_name)
    level = fields.Integer(default=1)
    life = fields.Float(default=100)
    smart = fields.Float(default=_calculate_random_num)
    power = fields.Float(default=_calculate_random_num)

    weapon = fields.Many2one("product.product")
    training = fields.Many2one("kill4city.training")
    in_city = fields.Many2one("kill4city.city",ondelete="set null")
    occupied = fields.Boolean(default=False)
    in_battle = fields.Boolean(default=False)
    is_plater = fields.Boolean(default=True)


class weapon(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    # name = fields.Char()
    damage = fields.Integer()
    # photo = fields.Image(max_width=100, max_height=100)
    use_by = fields.One2many("res.partner","weapon")
    is_weapon = fields.Boolean(default=True)

class conquer(models.Model):
    _name = 'kill4city.conquer'
    _description = 'kill4city.conquer'

    zone = fields.Many2one("kill4city.zone", required = True, ondelete='cascade')
    player = fields.Many2one("res.partner", required = True, ondelete='cascade')
    start_time = fields.Datetime(readonly=True)
    end_time = fields.Datetime(readonly=True)
    # end_time = fields.Datetime(compute='_calculate_end_time')
    percentage_conquers = fields.Float(default=0)
    player_life = fields.Float(default=0)
    player_life_at_start = fields.Float(default=0)
    in_battle = fields.Boolean(default=True)
    player_win = fields.Boolean(default=False)
    player_life_cost = fields.Integer(default=0)
    increment_zone_values = fields.Boolean(default=True)
    player_is_rescue_mood = fields.Boolean(default=False)

    @api.model
    def create(self,values):
        record = super(conquer, self).create(values)
        record.start_time = fields.Datetime.to_string(datetime.now())
        record.end_time = record._calculate_end_time()
        record.player_life = record.player.life
        record.player_life_at_start = record.player.life
        record.player.occupied = True
        return record

    # @api.depends('start_time','player','zone')
    def _calculate_end_time(self):
            for conquer in self:
                # Calculate how dangers is the player 
                player_calculate = ((conquer.player.level * conquer.player.power * conquer.player.smart) / 3)
                if conquer.player.weapon.damage != 0: # if is == 0 the player has no weapon
                    player_calculate = player_calculate + ((player_calculate * conquer.player.weapon.damage) / 100)
                # Calculate how dangers is the zone for the player
                zone_calculate = abs(((conquer.zone.level * conquer.zone.defense * conquer.zone.danger) / 3))
                # ... ... ... 
                # time_end_calculate = abs(zone_calculate - player_calculate)
                time_end_calculate = math.log(zone_calculate * player_calculate,2)
                if player_calculate > zone_calculate:
                    conquer.player_win = True
                    # print("conquer.player_life_cost => ",conquer.player_life_cost)
                conquer.player_life_cost = ((((100*zone_calculate)/player_calculate)/3)*2.2)

                # print("time_end_calculate =>" , time_end_calculate)
                # print("math.log(z* (p*w),2) =>  " , math.log(zone_calculate * player_calculate,2))
                # print("zone_calculate => ", zone_calculate)
                # print("player_calculate => ", player_calculate)
                # print("zone_calculate => ", zone_calculate)
                # time_end_calculate = math.log(1* (zone_calculate*player_calculate),2)

                return fields.Datetime.to_string(fields.Datetime.from_string(conquer.start_time) + timedelta(hours=time_end_calculate))
                    
    def calculate_time_difference_percentage(self):
        allConquer = self.search([])
        for c in allConquer:
            #Calculate the time difference between two times in minutes
            time_delta = (c.end_time - c.start_time)
            total_seconds = time_delta.total_seconds()
            total_minutes = total_seconds/60

            time_delta = (c.end_time - datetime.now())
            total_seconds = time_delta.total_seconds()
            minutes_from_now = total_seconds/60

            # Calculate the percentage of time elapsed
            elapsed_time_in_percent = ((100*(total_minutes - minutes_from_now))/total_minutes)
        return elapsed_time_in_percent

    def take_players_life(self):
        allConquer = self.search([])
        for c in allConquer:
            # percentage_of_life_cost = ((c.percentage_conquers*c.player_life_cost)/100)
            # life_cost_amount = ((100*percentage_of_life_cost)/c.player_life_cost)
            life_cost_amount = ((c.player_life_cost*c.percentage_conquers)/100)
        return c.player_life_at_start - life_cost_amount

    def player_loss_battle(self):
        allConquer = self.search([])
        for c in allConquer:
            # if player is premium:
                # print("recovering body..")
                # c.player.life = 1
                # si el personaje ha muerto a las 3 horas de empezar 
                # la conquesta su cuerpo tardara 1:30 en recuperarse
                # se llama a otro al cron de recuperacion
                # player_is_rescue_mood = True
            # else:
            c.player.life = 0
            c.player_life = 0
            c.in_battle = False
            c.player.occupied = False
            if c.increment_zone_values: #Revisar if cuando hagas el premioum
                c.zone.food += 1
                c.increment_zone_values = False

    @api.model
    def update_conquer(self):
        allConquer = self.search([('in_battle','=',True)])
        for c in allConquer:
            if c.player.life <= 0:
                c.player_loss_battle()                
            else:
                c.percentage_conquers = c.calculate_time_difference_percentage()
                c.zone.conquest = c.percentage_conquers
                c.player.life = c.take_players_life()
                c.player_life = c.player.life 
                # c.in_battle = False
            # reload page automatic not working :(
            # action = self.env.ref('kill4city.action_conquer_window').read()[0]
            print("CRON UPDATE DONE ======")
            # return action

    def increment(self):
        allConquer = self.search([])
        for c in allConquer:
            if c.player.life <= 0:
                c.player_loss_battle()                
            else:
                c.percentage_conquers = c.calculate_time_difference_percentage()
                c.player.life = c.take_players_life()
                c.player_life = c.player.life 
                # c.in_battle = False

class conquer_wizard(models.TransientModel):
    _name = 'kill4city.conquer_wizard'
    _description = 'Wizard of conquer'

    def _get_zone(self):
        city = self.env.context.get('zone_context')
        return city

    state = fields.Selection([('select_zone','Zone'),('select_player','Player'),('select_info','Info')], default = 'select_zone')

    zone = fields.Many2one("kill4city.zone", default = _get_zone)
    player = fields.Many2one("res.partner", ondelete='cascade')
    start_time = fields.Datetime(default=fields.Datetime.to_string(datetime.now()),readonly=True)
    end_time = fields.Datetime(compute="_calculate_end_time",readonly=True)



    @api.depends('start_time','player','zone')
    def _calculate_end_time(self):
            for conquer in self:
                print("len =>>>>>>",len(conquer.player)) #aqui
                

    def done(self):
        conquer = self.env['kill4city.conquer'].create({
            'zone': self.zone.id,
            'player': self.player.id
        })
        return {
            'name': 'kill4city conquer',
            'type': 'ir.actions.act_window',
            'res_model': 'kill4city.conquer',
            'res_id': conquer.id,
            'view_mode': 'form',
            'target': 'current'
        }
        print("fuc Done")



    def next(self):
        state = self.state
        if state == 'select_zone':
            self.state = 'select_player'
        elif state == 'select_player':
            self.state = 'select_info'

        return {
            'name': 'Negocity travel wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': self._context
        } 

    def previous(self):
        state = self.state
        if state == 'select_info':
            self.state = 'select_player'
        elif state == 'select_player':
            self.state = 'select_zone'


        return {
        'name': 'Negocity travel wizard action',
        'type': 'ir.actions.act_window',
        'res_model': self._name,
        'res_id': self.id,
        'view_mode': 'form',
        'target': 'new',
        'context': self._context
        }