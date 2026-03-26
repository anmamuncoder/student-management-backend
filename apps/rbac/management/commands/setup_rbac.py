from django.core.management.base import BaseCommand
from django.db import transaction

from apps.rbac.models import Permission, Role, UserRole
from apps.rbac.config import INITIAL_PERMISSIONS, INITIAL_ROLES


class Command(BaseCommand):
    help = 'Seed initial RBAC permissions and roles into the database.'

    def add_arguments(self, parser): 
        # setup + roles reset
        # python manage.py setup_rbac --reset-roles True/False

        parser.add_argument(
            '--reset-roles',
            action='store_true',
            help='Clear and re-assign all role permissions (non-destructive to users).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        
        # Step 1: Create permissions
        # Initial Permission created 
        self.stdout.write('Creating permissions...')

        perm_created = 0
        for p in INITIAL_PERMISSIONS:
            _ , created = Permission.objects.get_or_create(slug=p['slug'],defaults={'name':p['name'],'resource': p['resource'],'action':   p['action']})
            if created:
                perm_created += 1
                self.stdout.write(f"    + {p['slug']}")
        
        # Output Report
        self.stdout.write(
            self.style.SUCCESS(
                f"  {perm_created} new permissions created!"
                f"({len(INITIAL_PERMISSIONS)-perm_created} already existed.)"
            )
        )

        # Step 2: Create roles + assign permissions
        self.stdout.write('Creating roles...')
       
        import re 
        for role_name, perm_slugs in INITIAL_ROLES.items():
            slug = re.sub(r'[^a-z0-9]+', '-', role_name.lower()).strip('-')
            role, created = Role.objects.get_or_create(slug=slug, defaults={'name': role_name.title()})

            if options['reset_roles'] or created:
                perms = Permission.objects.filter(slug__in=perm_slugs)
                role.permissions.set(perms)
                missing = set(perm_slugs) - set(perms.values_list('slug', flat=True))
                
                if missing:
                    self.stdout.write(self.style.WARNING(
                        f"  !Role '{role_name}' missing permissions: {missing}"
                    ))
                action_label = 'created' if created else 'updated'
                self.stdout.write(f"  {'+'  if created else '~'} Role '{role_name}' {action_label} with {perms.count()} permissions")
            
            else:
                self.stdout.write(f"  Role '{role_name}' already exists (skipped)")
 

        self.stdout.write(self.style.SUCCESS('\nSetup complete!\n'))
        self.stdout.write('Run with --reset-roles to re-sync role permissions.')
        self.stdout.write('Run with --assign-admin user@email.com to assign admin role.\n')
