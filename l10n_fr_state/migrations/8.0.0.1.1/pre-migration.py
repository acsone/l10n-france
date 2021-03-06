# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Akretion (http://www.akretion.com/)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


def migrate(cr, version):
    if not version:
        return

    # key : source region XMLID - value : destination region XMLID
    new_region_map = {
        'res_country_state_rhonealpes': 'res_country_state_auvergne',
        'res_country_state_champagneardenne': 'res_country_state_alsace',
        'res_country_state_lorraine': 'res_country_state_alsace',
        'res_country_state_limousin': 'res_country_state_aquitaine',
        'res_country_state_poitoucharentes': 'res_country_state_aquitaine',
        'res_country_state_franchecomte': 'res_country_state_bourgogne',
        'res_country_state_midipyrenees':
        'res_country_state_languedocroussillon',
        'res_country_state_picardie': 'res_country_state_nordpasdecalais',
        'res_country_state_hautenormandie': 'res_country_state_bassenormandie',
        }

    # same as new_region_map but with IDs instead of XMLIDs
    new_region_map_id = {}

    for src, dest in new_region_map.iteritems():
        cr.execute("""
            SELECT res_id from ir_model_data where model='res.country.state'
            AND module='l10n_fr_state' AND name=%s
            """, (src, ))
        res_src_id = cr.fetchall()
        cr.execute("""
            SELECT res_id from ir_model_data where model='res.country.state'
            AND module='l10n_fr_state' AND name=%s
            """, (dest, ))
        res_dest_id = cr.fetchall()
        if res_src_id and res_dest_id:
            new_region_map_id[res_src_id[0][0]] = res_dest_id[0][0]

    for src_id, dest_id in new_region_map_id.iteritems():
        cr.execute("""
            UPDATE res_partner set state_id=%s where state_id=%s
            """, (dest_id, src_id))

        cr.execute("""
            SELECT id from ir_model where model='res.country.department'
            """)
        dpt = cr.fetchall()
        if dpt:
            cr.execute("""
                UPDATE res_country_department set state_id=%s where state_id=%s
                """, (dest_id, src_id))

        cr.execute("""
            SELECT id from ir_model where model='res.better.zip'
            """)
        bzip = cr.fetchall()
        if bzip:
            cr.execute("""
                UPDATE res_better_zip set state_id=%s where state_id=%s
                """, (dest_id, src_id))
