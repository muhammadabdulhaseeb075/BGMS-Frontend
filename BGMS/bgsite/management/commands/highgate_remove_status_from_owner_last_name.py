import sys
import traceback
import calendar

from django.core.management.base import BaseCommand

from bgsite.models import GraveOwner, OwnerStatus
from BGMS.utils import date_elements_to_full_date

''' GraveOwner - removes status from last_name and puts into status field '''

''' Run using : 'python manage.py tenant_command highgate_remove_status_from_owner_last_name --schema=highgate' '''

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
        # get statuses
        exor,created = OwnerStatus.objects.get_or_create(status='Exor')
        non_exor,created = OwnerStatus.objects.get_or_create(status='Non-Exor')
        admin,created = OwnerStatus.objects.get_or_create(status='Admin')
        trustee,created = OwnerStatus.objects.get_or_create(status='Trustee')
        widow,created = OwnerStatus.objects.get_or_create(status='Widow')
        spinster,created = OwnerStatus.objects.get_or_create(status='Spinster')
        extrx,created = OwnerStatus.objects.get_or_create(status='Extrx')
        not_extrx,created = OwnerStatus.objects.get_or_create(status='Not Extrx')
        exx,created = OwnerStatus.objects.get_or_create(status='Exx')
        not_exx,created = OwnerStatus.objects.get_or_create(status='Not Exx')
        admx,created = OwnerStatus.objects.get_or_create(status='Admx')
        extxs,created = OwnerStatus.objects.get_or_create(status='Extxs')
        not_extxs,created = OwnerStatus.objects.get_or_create(status='Not Extxs')
        tenants_in_common,created = OwnerStatus.objects.get_or_create(status='Tenants in Common')
        by_assignment,created = OwnerStatus.objects.get_or_create(status='By Assignment')
        devisee_in_trust,created = OwnerStatus.objects.get_or_create(status='Devisee in Trust')
        devisee,created = OwnerStatus.objects.get_or_create(status='Devisee')
        devisers_in_trust,created = OwnerStatus.objects.get_or_create(status='Devisers in Trust')
        universal_legatee,created = OwnerStatus.objects.get_or_create(status='Universal Legatee')
        executrix,created = OwnerStatus.objects.get_or_create(status='Executrix')
        executor,created = OwnerStatus.objects.get_or_create(status='Executor')
        power_of_attorney,created = OwnerStatus.objects.get_or_create(status='Power of Attorney')
        extrix,created = OwnerStatus.objects.get_or_create(status='Extrix')
        by_probate,created = OwnerStatus.objects.get_or_create(status='By Probate')
        by_statutory_declaration,created = OwnerStatus.objects.get_or_create(status='By Statutory Declaration')
        by_virtue_of_declaration,created = OwnerStatus.objects.get_or_create(status='By Virtue of Declaration')

        grave_owners = GraveOwner.objects.filter(person__last_name__contains='(')
        total = grave_owners.count()
        count = 0
        
        # Note: this could be written much more efficiently, but as it's a one time process, so it doesn't matter
        for grave_owner in grave_owners:
            
            owner_last_name = grave_owner.owner.last_name
            
            if 'SOLE' in owner_last_name:
                owner_last_name = owner_last_name.replace('SOLE','')
            
            
            if 'OWNERS IN TRUST' in owner_last_name:
                pass
            elif 'OWNERS' in owner_last_name:
                owner_last_name = owner_last_name.replace('OWNERS','')
            elif 'OWNER' in owner_last_name:
                owner_last_name = owner_last_name.replace('OWNER','')
            
            if 'NOT EXORS' in owner_last_name:
                grave_owner.owner_status.add(non_exor)
                owner_last_name = owner_last_name.replace('NOT EXORS','')
            elif 'NOT EXOR' in owner_last_name:
                grave_owner.owner_status.add(non_exor)
                owner_last_name = owner_last_name.replace('NOT EXOR','')
            elif 'NON-EXOR' in owner_last_name:
                grave_owner.owner_status.add(non_exor)
                owner_last_name = owner_last_name.replace('NON-EXOR','')
            
            if 'EXORS' in owner_last_name:
                grave_owner.owner_status.add(exor)
                owner_last_name = owner_last_name.replace('EXORS','')
            elif 'EXOR' in owner_last_name:
                grave_owner.owner_status.add(exor)
                owner_last_name = owner_last_name.replace('EXOR','')
            elif "EX'ORS" in owner_last_name:
                grave_owner.owner_status.add(exor)
                owner_last_name = owner_last_name.replace("EX'ORS",'')
            
            if 'WIDOW' in owner_last_name:
                grave_owner.owner_status.add(widow)
                owner_last_name = owner_last_name.replace('WIDOW','')
            elif 'WODOW' in owner_last_name:
                grave_owner.owner_status.add(widow)
                owner_last_name = owner_last_name.replace('WODOW','')
            
            if 'SPINSTER' in owner_last_name:
                grave_owner.owner_status.add(spinster)
                owner_last_name = owner_last_name.replace('SPINSTER','')
            elif 'SPINISTER' in owner_last_name:
                grave_owner.owner_status.add(spinster)
                owner_last_name = owner_last_name.replace('SPINISTER','')
            elif 'SINSTER' in owner_last_name:
                grave_owner.owner_status.add(spinster)
                owner_last_name = owner_last_name.replace('SINSTER','')
            elif 'SPNSTER' in owner_last_name:
                grave_owner.owner_status.add(spinster)
                owner_last_name = owner_last_name.replace('SPNSTER','')
            elif 'SPINSTRS' in owner_last_name:
                grave_owner.owner_status.add(spinster)
                owner_last_name = owner_last_name.replace('SPINSTRS','')
            
            if 'ADMINS' in owner_last_name:
                grave_owner.owner_status.add(admin)
                owner_last_name = owner_last_name.replace('ADMINS','')
            elif 'ADMIN' in owner_last_name:
                grave_owner.owner_status.add(admin)
                owner_last_name = owner_last_name.replace('ADMIN','')
            
            if 'SURVIVING TRUSTEES' in owner_last_name:
                grave_owner.owner_status.add(trustee)
                owner_last_name = owner_last_name.replace('SURVIVING TRUSTEES','')
            elif 'AS TRUSTEES' in owner_last_name:
                grave_owner.owner_status.add(trustee)
                owner_last_name = owner_last_name.replace('AS TRUSTEES','')
            elif 'TRUSTEES' in owner_last_name:
                grave_owner.owner_status.add(trustee)
                owner_last_name = owner_last_name.replace('TRUSTEES','')
            elif 'TRUSTEE' in owner_last_name:
                grave_owner.owner_status.add(trustee)
                owner_last_name = owner_last_name.replace('TRUSTEE','')
            elif 'TRRUSTEE' in owner_last_name:
                grave_owner.owner_status.add(trustee)
                owner_last_name = owner_last_name.replace('TRRUSTEE','')
            
            if 'NOT EXTRXS' in owner_last_name:
                grave_owner.owner_status.add(not_extrx)
                owner_last_name = owner_last_name.replace('NOT EXTRXS','')
            elif 'NOT EXTRX' in owner_last_name:
                grave_owner.owner_status.add(not_extrx)
                owner_last_name = owner_last_name.replace('NOT EXTRX','')
            elif 'NON-EXTRX' in owner_last_name:
                grave_owner.owner_status.add(not_extrx)
                owner_last_name = owner_last_name.replace('NON-EXTRX','')
            
            if 'EXTRXS' in owner_last_name:
                grave_owner.owner_status.add(extrx)
                owner_last_name = owner_last_name.replace('EXTRXS','')
            elif 'EXTRX' in owner_last_name:
                grave_owner.owner_status.add(extrx)
                owner_last_name = owner_last_name.replace('EXTRX','')
            
            if 'NOT EXXS' in owner_last_name:
                grave_owner.owner_status.add(not_exx)
                owner_last_name = owner_last_name.replace('NOT EXXS','')
            elif 'NOT EXX' in owner_last_name:
                grave_owner.owner_status.add(not_exx)
                owner_last_name = owner_last_name.replace('NOT EXX','')
            elif 'NON-EXX' in owner_last_name:
                grave_owner.owner_status.add(not_exx)
                owner_last_name = owner_last_name.replace('NON-EXX','')
            
            if 'EXXS' in owner_last_name:
                grave_owner.owner_status.add(exx)
                owner_last_name = owner_last_name.replace('EXXS','')
            elif 'EXX' in owner_last_name:
                grave_owner.owner_status.add(exx)
                owner_last_name = owner_last_name.replace('EXX','')
            
            if 'ADMXS' in owner_last_name:
                grave_owner.owner_status.add(admx)
                owner_last_name = owner_last_name.replace('ADMXS','')
            elif 'ADMX' in owner_last_name:
                grave_owner.owner_status.add(admx)
                owner_last_name = owner_last_name.replace('ADMX','')
            
            if 'NOT EXTXES' in owner_last_name:
                grave_owner.owner_status.add(not_extxs)
                owner_last_name = owner_last_name.replace('NOT EXTXES','')
            elif 'NOT EXTXS' in owner_last_name:
                grave_owner.owner_status.add(not_extxs)
                owner_last_name = owner_last_name.replace('NOT EXTXS','')
            elif 'NOT EXTX' in owner_last_name:
                grave_owner.owner_status.add(not_extxs)
                owner_last_name = owner_last_name.replace('NOT EXTX','')
            elif 'NON-EXTX' in owner_last_name:
                grave_owner.owner_status.add(not_extxs)
                owner_last_name = owner_last_name.replace('NON-EXTX','')
            
            if 'EXTXES' in owner_last_name:
                grave_owner.owner_status.add(extxs)
                owner_last_name = owner_last_name.replace('EXTXES','')
            elif 'EXTXS' in owner_last_name:
                grave_owner.owner_status.add(extxs)
                owner_last_name = owner_last_name.replace('EXTXS','')
            elif 'EXTX' in owner_last_name:
                grave_owner.owner_status.add(extxs)
                owner_last_name = owner_last_name.replace('EXTX','')
            
            if 'TENANTS IN COMMON' in owner_last_name:
                grave_owner.owner_status.add(tenants_in_common)
                owner_last_name = owner_last_name.replace('TENANTS IN COMMON','')
            elif 'TENANTS-IN-COMMON' in owner_last_name:
                grave_owner.owner_status.add(tenants_in_common)
                owner_last_name = owner_last_name.replace('TENANTS-IN-COMMON','')
            elif 'TENANT IN COMMON' in owner_last_name:
                grave_owner.owner_status.add(tenants_in_common)
                owner_last_name = owner_last_name.replace('TENANT IN COMMON','')
            
            if 'BY ASSIGNMENT' in owner_last_name:
                grave_owner.owner_status.add(by_assignment)
                owner_last_name = owner_last_name.replace('BY ASSIGNMENT','')
            
            if 'DEVIZEE IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisee_in_trust)
                owner_last_name = owner_last_name.replace('DEVIZEE IN TRUST','')
            elif 'DEVIZEES IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisee_in_trust)
                owner_last_name = owner_last_name.replace('DEVIZEES IN TRUST','')
            elif 'DEVISEE IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisee_in_trust)
                owner_last_name = owner_last_name.replace('DEVISEE IN TRUST','')
            elif 'DEVISEES IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisee_in_trust)
                owner_last_name = owner_last_name.replace('DEVISEES IN TRUST','')
            elif 'DIVISEES IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisee_in_trust)
                owner_last_name = owner_last_name.replace('DIVISEES IN TRUST','')
            elif 'DIVISEE IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisee_in_trust)
                owner_last_name = owner_last_name.replace('DIVISEE IN TRUST','')
            
            if 'DEVIZERS IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisers_in_trust)
                owner_last_name = owner_last_name.replace('DEVIZERS IN TRUST','')
            elif 'DEVIZER IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisers_in_trust)
                owner_last_name = owner_last_name.replace('DEVIZER IN TRUST','')
            elif 'DIVIZERS IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisers_in_trust)
                owner_last_name = owner_last_name.replace('DIVIZERS IN TRUST','')
            elif 'DIVIZER IN TRUST' in owner_last_name:
                grave_owner.owner_status.add(devisers_in_trust)
                owner_last_name = owner_last_name.replace('DIVIZER IN TRUST','')
            
            if 'DEVISEES' in owner_last_name:
                grave_owner.owner_status.add(devisee)
                owner_last_name = owner_last_name.replace('DEVISEES','')
            elif 'DEVISEE' in owner_last_name:
                grave_owner.owner_status.add(devisee)
                owner_last_name = owner_last_name.replace('DEVISEE','')
            elif 'DEVIZEES' in owner_last_name:
                grave_owner.owner_status.add(devisee)
                owner_last_name = owner_last_name.replace('DEVIZEES','')
            elif 'DEVIZEE' in owner_last_name:
                grave_owner.owner_status.add(devisee)
                owner_last_name = owner_last_name.replace('DEVIZEE','')
                
            if 'UNIVERSAL LEGATEE' in owner_last_name:
                grave_owner.owner_status.add(universal_legatee)
                owner_last_name = owner_last_name.replace('UNIVERSAL LEGATEE','')
                
            if 'EXECUTRIX' in owner_last_name:
                grave_owner.owner_status.add(executrix)
                owner_last_name = owner_last_name.replace('EXECUTRIX','')
                
            if 'EXECUTOR' in owner_last_name:
                grave_owner.owner_status.add(executor)
                owner_last_name = owner_last_name.replace('EXECUTOR','')
            elif 'EXECS' in owner_last_name:
                grave_owner.owner_status.add(executor)
                owner_last_name = owner_last_name.replace('EXECS','')
            elif 'EXEC' in owner_last_name:
                grave_owner.owner_status.add(executor)
                owner_last_name = owner_last_name.replace('EXEC','')
                
            if 'POWER OF ATTORNEY' in owner_last_name:
                grave_owner.owner_status.add(power_of_attorney)
                owner_last_name = owner_last_name.replace('POWER OF ATTORNEY','')
                
            if 'EXTRIX' in owner_last_name:
                grave_owner.owner_status.add(extrix)
                owner_last_name = owner_last_name.replace('EXTRIX','')
                
            if 'BY PROBATE' in owner_last_name:
                grave_owner.owner_status.add(by_probate)
                owner_last_name = owner_last_name.replace('BY PROBATE','')
                
            if 'BY STATUTORY DECLARATION' in owner_last_name:
                grave_owner.owner_status.add(by_statutory_declaration)
                owner_last_name = owner_last_name.replace('BY STATUTORY DECLARATION','')
            elif 'BY STAT DEC' in owner_last_name:
                grave_owner.owner_status.add(by_statutory_declaration)
                owner_last_name = owner_last_name.replace('BY STAT DEC','')
                
            if 'BY VIRTUE OF DECLARATION' in owner_last_name:
                grave_owner.owner_status.add(by_virtue_of_declaration)
                owner_last_name = owner_last_name.replace('BY VIRTUE OF DECLARATION','')
            
            if '(,' in owner_last_name:
                owner_last_name = owner_last_name.replace('(,','(')
            
            if '( ' in owner_last_name:
                owner_last_name = owner_last_name.replace('( ','(')
            
            if ' )' in owner_last_name:
                owner_last_name = owner_last_name.replace(' )',')')
            
            if ',)' in owner_last_name:
                owner_last_name = owner_last_name.replace(',)',')')
            
            if '()' in owner_last_name:
                owner_last_name = owner_last_name.replace('()','')
            elif '(S)' in owner_last_name:
                owner_last_name = owner_last_name.replace('(S)','')
            elif '( )' in owner_last_name:
                owner_last_name = owner_last_name.replace('( )','')
            elif '( & )' in owner_last_name:
                owner_last_name = owner_last_name.replace('( & )','')
            elif '( AND )' in owner_last_name:
                owner_last_name = owner_last_name.replace('( AND )','')
            elif '(.)' in owner_last_name:
                owner_last_name = owner_last_name.replace('(.)','')
            elif '( .)' in owner_last_name:
                owner_last_name = owner_last_name.replace('( .)','')
            elif '(. & )' in owner_last_name:
                owner_last_name = owner_last_name.replace('(. & )','')
            elif '(, )' in owner_last_name:
                owner_last_name = owner_last_name.replace('(, )','')
            elif '(?)' in owner_last_name:
                owner_last_name = owner_last_name.replace('(?)','')
            elif '(&)' in owner_last_name:
                owner_last_name = owner_last_name.replace('(&)','')
            elif '(& )' in owner_last_name:
                owner_last_name = owner_last_name.replace('(& )','')
            
            owner_last_name = owner_last_name.strip()
            
            count+=1
            msg = str(count) + ' of ' + str(total)
            
            if not grave_owner.owner.last_name == owner_last_name:
                msg += ': ' + grave_owner.owner.last_name + ' changed to ' + owner_last_name
                print (msg)
            
            grave_owner.owner.last_name = owner_last_name
            grave_owner.owner.save()
            grave_owner.save()

    except Exception as e:
        print(traceback.format_exc())