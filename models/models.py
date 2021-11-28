# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random


class zone(models.Model):
    _name = 'kill4city.zone'
    _description = 'kill4city.zone'

    def _generate_town_name(self):
        towns = ["Oscoz","Torrelara","Coscullano","Cicera","Haedillo","Eustaquios","Navarredondilla","Elda","Garayolza","Marne","Santiorjo","Delfiá","Malá","Noia","Puertas","Sardas","Felechosas","Bujursot","Betolaza","Batiao","Berzosa","Rigueira","Guaso","Bode","Logrosa","Vilamitjana","Cogela","Royo","Solmayor","Daneiro","Fornes","Medal","Infesta","Ludrio","Torregorda","Cereijido","Sanjurjo","Corres","Espasantes","Igea","Pierres","Carabias","Concha","Torleque","Viella","Arro","Cegama","Jubia","Torquiendo","Loja"]
        return random.choice(towns)

    def _generate_zone_lavel(salf):
        # Futura mejora => Mirar la cantidad de zonas que tiene una ciudad 
                            # para generar minimo un 3% de zonas con un nivel 1 y
                            # un 5% de zonas al nivel 100;
                            # => Mirar el nivel del jugador para crear zonas apartit de su nuvel
                            
        return random.randint(0,100)
    


    lavel = fields.Integer(default=_generate_zone_lavel)
    
    # def _generate_live_heal(lavel):
    #     # Revisar
    #     return 202 * 2


    name = fields.Char(default=_generate_town_name)
    conquest = fields.Float()
    status = fields.Char(default="Invaded")
    food = fields.Integer(default=404)
    # live_heal = fields.Integer(default=_generate_live_heal)
    # liveHeal = fields.Integer(default=_generate_live_heal,readonly=True)

    city = fields.Many2one("kill4city.city")

    def conquer(self):
        print("Hallo")
        

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





class player(models.Model):
    _name = 'kill4city.player'
    _description = 'kill4city.player'

    def _generate_player_name(self):
        ranName = ["Isabel Saldaña","Mariam Contador","Noemi Monte","Vanessa Villalobos","Nerea Racionero","Uxia Barbero","Fatima Marinero","Nora Balderas","Ana Isabel Sallent","Ainoa Carpentier","Angel Hernández","Iago Jurado","Jose Maria Valderas","Alonso Panadero","Matias Villalba","Isaac Alcaide","Kevin Rabellino","Francisco Padrón","Jordi Val","Salvador Balderas","Gerard Morterero","Miguel Mallén","Alonso del Valle","Pol Domínguez","Jon Ferrero","Ramon Fuster o Fusté","Oliver Hernández","Sergi Bielsa","Rodrigo Enríquez","Pau Ascaso","Mar Valverde","Gabriela Santolaria","Patricia Ordóñez","Judith Siurana","Judit Villalobos","Mireya Pajarero","Clara Racionero","Carmen Maria Molinero","Zaira Martín","Neus Peña"]
        return random.choice(ranName)

    name = fields.Char(default=_generate_player_name)
    lavel = fields.Integer(default=1)
    life = fields.Integer(default=20)
    # weapon = fields.Integer(default=404)
    weapon = fields.Many2one("kill4city.weapon")
    in_city = fields.Many2one("kill4city.city",ondelete="set null")
    #///aquiiii
    
    # @api.depends('city')
    # def _get_city_available(self):
    #     for b in self:
    #         b.workers_available = (b.city.survivors - b.workers).filtered(
    #             lambda w: len(w.city.buildings.workers.filtered(
    #                 lambda ww: ww.id == w.id))
    #                 ==0)


class weapon(models.Model):
    _name = 'kill4city.weapon'
    _description = 'kill4city.weapon'

    name = fields.Char()
    damage = fields.Integer()
    photo = fields.Image(max_width=100, max_height=100)
    use_by = fields.One2many("kill4city.player","weapon")






# class kill4city(models.Model):
#     _name = 'kill4city.kill4city'
#     _description = 'kill4city.kill4city'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)  #para usar el store=True hay que haver que la funcion dependa de un valor depends("name")
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
