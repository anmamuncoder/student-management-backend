URL_PERMISSION_MAP = [ 
    # Accounts / Users
    (r'/api/v1/accounts/users/', 'accounts_users'), 
    (r'/api/v1/accounts/ranks/', 'accounts_ranks'),  # All Method

    # Self acc/accountsount actions (standard naming)
    (r'/api/v1/accounts/password/change/', 'self_account'), # - PUT
    (r'/api/v1/accounts/email/change/', 'self_account'), # POST
    (r'/api/v1/accounts/email/change/verify/', 'self_account'), # POST

    # RBAC
    (r'/api/v1/rbac/roles/', 'rbac_roles'),
    (r'/api/v1/rbac/permissions/', 'rbac_permissions'),

    (r'/api/v1/rbac/permissions/self/', 'rbac_permissions_self'),   # GET only
    (r'/api/v1/rbac/user-roles-assign/', 'rbac_user_roles_assign'), # ALL methods

    # Students
    (r'/api/v1/students/students/', 'students_students'), # All Method
    (r'/api/v1/students/student-types/', 'students_student_types'), # All Method
    (r'/api/v1/students/student-groups/', 'students_student_groups'), # All Method
    (r'/api/v1/students/activities/', 'students_activities'), # All Method
    (r'/api/v1/students/spouses/', 'students_spouses'), # All Method
    (r'/api/v1/students/qualifications/', 'students_qualifications'), # All Method
    (r'/api/v1/students/bank-accounts/', 'students_bank_accounts'), # All Method
    (r'/api/v1/students/military-qualifications/', 'students_military_qualifications'), # All Method
    (r'/api/v1/students/service-records/', 'students_service_records'), # All Method
    (r'/api/v1/students/awards/', 'students_awards'), # All Method
    (r'/api/v1/students/un-missions/', 'students_un_missions'), # All Method
    (r'/api/v1/students/countries-visited/', 'students_countries_visited'), # All Method

    # Courses
    (r'/api/v1/courses/courses/', 'courses_courses'), # All Method
    (r'/api/v1/courses/subjects/', 'courses_subjects'), # All Method
    (r'/api/v1/courses/modules/', 'courses_modules'), # All Method
    (r'/api/v1/courses/syllabus/', 'courses_syllabus'), # All Method
    (r'/api/v1/courses/detail-syllabus/', 'courses_detail_syllabus'), # All Method
    (r'/api/v1/courses/batches/', 'courses_batches'), # All Method
]



HTTP_METHOD_ACTION_MAP = {
    'GET':'view',
    'POST':'create',
    'PUT':'update',
    'PATCH':'update',
    'DELETE':'delete',
    'HEAD':'view',
    'OPTIONS':'None',
}

EXEMPT_PATHS = [
    # Its Unauthenticated API'S
    r'^/api/v1/accounts/register/',
    r'^/api/v1/accounts/login/',
    r'^/api/v1/accounts/verify-otp/',
    r'^/api/v1/accounts/resend-otp/',
    r'^/api/v1/accounts/forgot-password/',
    r'^/api/v1/accounts/verify-reset-otp/',
    r'^/api/v1/accounts/reset-password/',
    r'^/api/v1/accounts/refresh/',

    
    r'^/admin/',
    r'^/api/schema/',
    r'^/api/docs/',
    r'^/api/redoc/',
    # r'^/health/',
]

# That will be create with for custom
# python manage.py setup_rbac 
# python manage.py setup_rbac --reset-roles True/False

# ------------ INITIAL SEED DATA ---------------

INITIAL_PERMISSIONS = [

    # --------------------------
    # ACCOUNTS - USERS
    # --------------------------
    {'name': 'View users',   'resource': 'accounts_users', 'action': 'view',   'slug': 'accounts_users:view'},
    {'name': 'Create users', 'resource': 'accounts_users', 'action': 'create', 'slug': 'accounts_users:create'},
    {'name': 'Update users', 'resource': 'accounts_users', 'action': 'update', 'slug': 'accounts_users:update'},
    {'name': 'Delete users', 'resource': 'accounts_users', 'action': 'delete', 'slug': 'accounts_users:delete'},

    # ACCOUNTS - RANKS
    {'name': 'View ranks',   'resource': 'accounts_ranks', 'action': 'view',   'slug': 'accounts_ranks:view'},
    {'name': 'Create ranks', 'resource': 'accounts_ranks', 'action': 'create', 'slug': 'accounts_ranks:create'},
    {'name': 'Update ranks', 'resource': 'accounts_ranks', 'action': 'update', 'slug': 'accounts_ranks:update'},
    {'name': 'Delete ranks', 'resource': 'accounts_ranks', 'action': 'delete', 'slug': 'accounts_ranks:delete'},

    # --------------------------
    # SELF ACCOUNT
    # --------------------------
    {'name': 'Change password', 'resource': 'self_account', 'action': 'update', 'slug': 'self_account:update'},
    {'name': 'Change email',    'resource': 'self_account', 'action': 'create', 'slug': 'self_account:create'},
    # {'name': 'Verify email',    'resource': 'self_account', 'action': 'create', 'slug': 'self_account:create'},

    # --------------------------
    # RBAC - ROLES
    # --------------------------
    {'name': 'View roles',   'resource': 'rbac_roles', 'action': 'view',   'slug': 'rbac_roles:view'},
    {'name': 'Create roles', 'resource': 'rbac_roles', 'action': 'create', 'slug': 'rbac_roles:create'},
    {'name': 'Update roles', 'resource': 'rbac_roles', 'action': 'update', 'slug': 'rbac_roles:update'},
    {'name': 'Delete roles', 'resource': 'rbac_roles', 'action': 'delete', 'slug': 'rbac_roles:delete'},

    # RBAC - PERMISSIONS (read-only)
    {'name': 'View permissions', 'resource': 'rbac_permissions', 'action': 'view', 'slug': 'rbac_permissions:view'},

    {'name': 'View own permissions', 'resource': 'rbac_permissions_self', 'action': 'view', 'slug': 'rbac_permissions_self:view'},

    # User Role Assign
    {'name': 'View user role assignment',   'resource': 'rbac_user_roles_assign', 'action': 'view',   'slug': 'rbac_user_roles_assign:view'},
    {'name': 'Assign user roles',           'resource': 'rbac_user_roles_assign', 'action': 'create', 'slug': 'rbac_user_roles_assign:create'},
    {'name': 'Update user roles',           'resource': 'rbac_user_roles_assign', 'action': 'update', 'slug': 'rbac_user_roles_assign:update'},
    {'name': 'Remove user roles',           'resource': 'rbac_user_roles_assign', 'action': 'delete', 'slug': 'rbac_user_roles_assign:delete'},

    # --------------------------
    # STUDENTS
    # --------------------------

    # students_students
    {'name': 'View students',   'resource': 'students_students', 'action': 'view',   'slug': 'students_students:view'},
    {'name': 'Create students', 'resource': 'students_students', 'action': 'create', 'slug': 'students_students:create'},
    {'name': 'Update students', 'resource': 'students_students', 'action': 'update', 'slug': 'students_students:update'},
    {'name': 'Delete students', 'resource': 'students_students', 'action': 'delete', 'slug': 'students_students:delete'},

    # student_types
    {'name': 'View student types',   'resource': 'students_student_types', 'action': 'view',   'slug': 'students_student_types:view'},
    {'name': 'Create student types', 'resource': 'students_student_types', 'action': 'create', 'slug': 'students_student_types:create'},
    {'name': 'Update student types', 'resource': 'students_student_types', 'action': 'update', 'slug': 'students_student_types:update'},
    {'name': 'Delete student types', 'resource': 'students_student_types', 'action': 'delete', 'slug': 'students_student_types:delete'},

    # student_groups
    {'name': 'View student groups',   'resource': 'students_student_groups', 'action': 'view',   'slug': 'students_student_groups:view'},
    {'name': 'Create student groups', 'resource': 'students_student_groups', 'action': 'create', 'slug': 'students_student_groups:create'},
    {'name': 'Update student groups', 'resource': 'students_student_groups', 'action': 'update', 'slug': 'students_student_groups:update'},
    {'name': 'Delete student groups', 'resource': 'students_student_groups', 'action': 'delete', 'slug': 'students_student_groups:delete'},

    # activities
    {'name': 'View activities',   'resource': 'students_activities', 'action': 'view',   'slug': 'students_activities:view'},
    {'name': 'Create activities', 'resource': 'students_activities', 'action': 'create', 'slug': 'students_activities:create'},
    {'name': 'Update activities', 'resource': 'students_activities', 'action': 'update', 'slug': 'students_activities:update'},
    {'name': 'Delete activities', 'resource': 'students_activities', 'action': 'delete', 'slug': 'students_activities:delete'},

    # spouses
    {'name': 'View spouses',   'resource': 'students_spouses', 'action': 'view',   'slug': 'students_spouses:view'},
    {'name': 'Create spouses', 'resource': 'students_spouses', 'action': 'create', 'slug': 'students_spouses:create'},
    {'name': 'Update spouses', 'resource': 'students_spouses', 'action': 'update', 'slug': 'students_spouses:update'},
    {'name': 'Delete spouses', 'resource': 'students_spouses', 'action': 'delete', 'slug': 'students_spouses:delete'},

    # qualifications
    {'name': 'View qualifications',   'resource': 'students_qualifications', 'action': 'view',   'slug': 'students_qualifications:view'},
    {'name': 'Create qualifications', 'resource': 'students_qualifications', 'action': 'create', 'slug': 'students_qualifications:create'},
    {'name': 'Update qualifications', 'resource': 'students_qualifications', 'action': 'update', 'slug': 'students_qualifications:update'},
    {'name': 'Delete qualifications', 'resource': 'students_qualifications', 'action': 'delete', 'slug': 'students_qualifications:delete'},

    # bank_accounts
    {'name': 'View bank accounts',   'resource': 'students_bank_accounts', 'action': 'view',   'slug': 'students_bank_accounts:view'},
    {'name': 'Create bank accounts','resource': 'students_bank_accounts', 'action': 'create', 'slug': 'students_bank_accounts:create'},
    {'name': 'Update bank accounts','resource': 'students_bank_accounts', 'action': 'update', 'slug': 'students_bank_accounts:update'},
    {'name': 'Delete bank accounts','resource': 'students_bank_accounts', 'action': 'delete', 'slug': 'students_bank_accounts:delete'},

    # military_qualifications
    {'name': 'View military qualifications',   'resource': 'students_military_qualifications', 'action': 'view',   'slug': 'students_military_qualifications:view'},
    {'name': 'Create military qualifications', 'resource': 'students_military_qualifications', 'action': 'create', 'slug': 'students_military_qualifications:create'},
    {'name': 'Update military qualifications', 'resource': 'students_military_qualifications', 'action': 'update', 'slug': 'students_military_qualifications:update'},
    {'name': 'Delete military qualifications', 'resource': 'students_military_qualifications', 'action': 'delete', 'slug': 'students_military_qualifications:delete'},

    # service_records
    {'name': 'View service records',   'resource': 'students_service_records', 'action': 'view',   'slug': 'students_service_records:view'},
    {'name': 'Create service records', 'resource': 'students_service_records', 'action': 'create', 'slug': 'students_service_records:create'},
    {'name': 'Update service records', 'resource': 'students_service_records', 'action': 'update', 'slug': 'students_service_records:update'},
    {'name': 'Delete service records', 'resource': 'students_service_records', 'action': 'delete', 'slug': 'students_service_records:delete'},

    # awards
    {'name': 'View awards',   'resource': 'students_awards', 'action': 'view',   'slug': 'students_awards:view'},
    {'name': 'Create awards', 'resource': 'students_awards', 'action': 'create', 'slug': 'students_awards:create'},
    {'name': 'Update awards', 'resource': 'students_awards', 'action': 'update', 'slug': 'students_awards:update'},
    {'name': 'Delete awards', 'resource': 'students_awards', 'action': 'delete', 'slug': 'students_awards:delete'},

    # un_missions
    {'name': 'View UN missions',   'resource': 'students_un_missions', 'action': 'view',   'slug': 'students_un_missions:view'},
    {'name': 'Create UN missions', 'resource': 'students_un_missions', 'action': 'create', 'slug': 'students_un_missions:create'},
    {'name': 'Update UN missions', 'resource': 'students_un_missions', 'action': 'update', 'slug': 'students_un_missions:update'},
    {'name': 'Delete UN missions', 'resource': 'students_un_missions', 'action': 'delete', 'slug': 'students_un_missions:delete'},

    # countries_visited
    {'name': 'View countries visited',   'resource': 'students_countries_visited', 'action': 'view',   'slug': 'students_countries_visited:view'},
    {'name': 'Create countries visited', 'resource': 'students_countries_visited', 'action': 'create', 'slug': 'students_countries_visited:create'},
    {'name': 'Update countries visited', 'resource': 'students_countries_visited', 'action': 'update', 'slug': 'students_countries_visited:update'},
    {'name': 'Delete countries visited', 'resource': 'students_countries_visited', 'action': 'delete', 'slug': 'students_countries_visited:delete'},

    # ------------------------
    # COURSES
    # ------------------------

    # courses
    {'name': 'View courses',   'resource': 'courses_courses', 'action': 'view',   'slug': 'courses_courses:view'},
    {'name': 'Create courses', 'resource': 'courses_courses', 'action': 'create', 'slug': 'courses_courses:create'},
    {'name': 'Update courses', 'resource': 'courses_courses', 'action': 'update', 'slug': 'courses_courses:update'},
    {'name': 'Delete courses', 'resource': 'courses_courses', 'action': 'delete', 'slug': 'courses_courses:delete'},

    # subjects
    {'name': 'View subjects',   'resource': 'courses_subjects', 'action': 'view',   'slug': 'courses_subjects:view'},
    {'name': 'Create subjects', 'resource': 'courses_subjects', 'action': 'create', 'slug': 'courses_subjects:create'},
    {'name': 'Update subjects', 'resource': 'courses_subjects', 'action': 'update', 'slug': 'courses_subjects:update'},
    {'name': 'Delete subjects', 'resource': 'courses_subjects', 'action': 'delete', 'slug': 'courses_subjects:delete'},

    # modules
    {'name': 'View modules',   'resource': 'courses_modules', 'action': 'view',   'slug': 'courses_modules:view'},
    {'name': 'Create modules', 'resource': 'courses_modules', 'action': 'create', 'slug': 'courses_modules:create'},
    {'name': 'Update modules', 'resource': 'courses_modules', 'action': 'update', 'slug': 'courses_modules:update'},
    {'name': 'Delete modules', 'resource': 'courses_modules', 'action': 'delete', 'slug': 'courses_modules:delete'},

    # syllabus
    {'name': 'View syllabus',   'resource': 'courses_syllabus', 'action': 'view',   'slug': 'courses_syllabus:view'},
    {'name': 'Create syllabus', 'resource': 'courses_syllabus', 'action': 'create', 'slug': 'courses_syllabus:create'},
    {'name': 'Update syllabus', 'resource': 'courses_syllabus', 'action': 'update', 'slug': 'courses_syllabus:update'},
    {'name': 'Delete syllabus', 'resource': 'courses_syllabus', 'action': 'delete', 'slug': 'courses_syllabus:delete'},

    # detail syllabus
    {'name': 'View detail syllabus',   'resource': 'courses_detail_syllabus', 'action': 'view',   'slug': 'courses_detail_syllabus:view'},
    {'name': 'Create detail syllabus', 'resource': 'courses_detail_syllabus', 'action': 'create', 'slug': 'courses_detail_syllabus:create'},
    {'name': 'Update detail syllabus', 'resource': 'courses_detail_syllabus', 'action': 'update', 'slug': 'courses_detail_syllabus:update'},
    {'name': 'Delete detail syllabus', 'resource': 'courses_detail_syllabus', 'action': 'delete', 'slug': 'courses_detail_syllabus:delete'},

    # batches
    {'name': 'View batches',   'resource': 'courses_batches', 'action': 'view',   'slug': 'courses_batches:view'},
    {'name': 'Create batches', 'resource': 'courses_batches', 'action': 'create', 'slug': 'courses_batches:create'},
    {'name': 'Update batches', 'resource': 'courses_batches', 'action': 'update', 'slug': 'courses_batches:update'},
    {'name': 'Delete batches', 'resource': 'courses_batches', 'action': 'delete', 'slug': 'courses_batches:delete'},
]



# -------------------------------
# INITIAL ROLES
# -------------------------------
# permission.slug list 

# Never create a separate 'Admin' role because superusers are already treated as admins.
# Define initial roles and their associated permissions.
INITIAL_ROLES = {

    # --------------------------
    # ADMIN (Full Access)
    # --------------------------
    'admin': [
        # Accounts
        'accounts_users:view','accounts_users:create','accounts_users:update','accounts_users:delete',
        'accounts_ranks:view','accounts_ranks:create','accounts_ranks:update','accounts_ranks:delete',

        # RBAC
        'rbac_roles:view','rbac_roles:create','rbac_roles:update','rbac_roles:delete',
        'rbac_permissions:view',

        # RBAC Self
        'rbac_permissions_self:view',
        # RBAC Assign
        'rbac_user_roles_assign:view',
        'rbac_user_roles_assign:create',
        'rbac_user_roles_assign:update',
        'rbac_user_roles_assign:delete',

        # Students (ALL)
        'students_students:view','students_students:create','students_students:update','students_students:delete',
        'students_student_types:view','students_student_types:create','students_student_types:update','students_student_types:delete',
        'students_student_groups:view','students_student_groups:create','students_student_groups:update','students_student_groups:delete',
        'students_activities:view','students_activities:create','students_activities:update','students_activities:delete',
        'students_spouses:view','students_spouses:create','students_spouses:update','students_spouses:delete',
        'students_qualifications:view','students_qualifications:create','students_qualifications:update','students_qualifications:delete',
        'students_bank_accounts:view','students_bank_accounts:create','students_bank_accounts:update','students_bank_accounts:delete',
        'students_military_qualifications:view','students_military_qualifications:create','students_military_qualifications:update','students_military_qualifications:delete',
        'students_service_records:view','students_service_records:create','students_service_records:update','students_service_records:delete',
        'students_awards:view','students_awards:create','students_awards:update','students_awards:delete',
        'students_un_missions:view','students_un_missions:create','students_un_missions:update','students_un_missions:delete',
        'students_countries_visited:view','students_countries_visited:create','students_countries_visited:update','students_countries_visited:delete',

        # Courses (ALL)
        'courses_courses:view','courses_courses:create','courses_courses:update','courses_courses:delete',
        'courses_subjects:view','courses_subjects:create','courses_subjects:update','courses_subjects:delete',
        'courses_modules:view','courses_modules:create','courses_modules:update','courses_modules:delete',
        'courses_syllabus:view','courses_syllabus:create','courses_syllabus:update','courses_syllabus:delete',
        'courses_detail_syllabus:view','courses_detail_syllabus:create','courses_detail_syllabus:update','courses_detail_syllabus:delete',
        'courses_batches:view','courses_batches:create','courses_batches:update','courses_batches:delete',

        # Self account
        'self_account:update','self_account:create',


    ],

    # --------------------------
    # STAFF (Operational user)
    # --------------------------
    'staff': [
        # Students (full manage)
        'students_students:view','students_students:create','students_students:update',
        'students_student_types:view','students_student_types:create','students_student_types:update',
        'students_student_groups:view','students_student_groups:create','students_student_groups:update',
        'students_activities:view','students_activities:create','students_activities:update',
        'students_spouses:view','students_spouses:create','students_spouses:update',
        'students_qualifications:view','students_qualifications:create','students_qualifications:update',
        'students_bank_accounts:view','students_bank_accounts:create','students_bank_accounts:update',
        'students_military_qualifications:view','students_military_qualifications:create','students_military_qualifications:update',
        'students_service_records:view','students_service_records:create','students_service_records:update',
        'students_awards:view','students_awards:create','students_awards:update',
        'students_un_missions:view','students_un_missions:create','students_un_missions:update',
        'students_countries_visited:view','students_countries_visited:create','students_countries_visited:update',

        # Courses (manage but no delete)
        'courses_courses:view','courses_courses:create','courses_courses:update',
        'courses_subjects:view','courses_subjects:create','courses_subjects:update',
        'courses_modules:view','courses_modules:create','courses_modules:update',
        'courses_syllabus:view','courses_syllabus:create','courses_syllabus:update',
        'courses_detail_syllabus:view','courses_detail_syllabus:create','courses_detail_syllabus:update',
        'courses_batches:view','courses_batches:create','courses_batches:update',

        # View users
        'accounts_users:view',

        # Self account
        'self_account:update','self_account:create',

        # Self Permission 
        'rbac_permissions_self:view'
    ],

    # --------------------------
    # STUDENT (Limited access)
    # --------------------------
    # 'student': [
    #     # View own/student data (no create/delete)
    #     'students_students:view',
    #     'students_activities:view',
    #     'students_qualifications:view',
    #     'students_awards:view',
    #     'students_un_missions:view',
    #     'students_countries_visited:view',

    #     # Courses (view only)
    #     'courses_courses:view',
    #     'courses_subjects:view',
    #     'courses_modules:view',
    #     'courses_syllabus:view',
    #     'courses_detail_syllabus:view',
    #     'courses_batches:view',

    #     # Self account
    #     'self_account:update','self_account:create',
    #     # Self Permission 
    #     'rbac_permissions_self:view'
    # ],

    # --------------------------
    # LIBRARIAN (Custom limited role)
    # --------------------------
    'librarian': [
        # Students (view only)
        'students_students:view',

        # Courses (view + limited manage)
        'courses_courses:view',
        'courses_subjects:view',
        'courses_modules:view',

        # Maybe manage syllabus (optional)
        'courses_syllabus:view','courses_syllabus:update',

        # Self account
        'self_account:update','self_account:create',
        
        # Self Permission 
        'rbac_permissions_self:view'
    ], 

    'teacher': [
        # Students (view + update limited info)
        'students_students:view',
        'students_students:update',
        'students_activities:view',
        'students_activities:create',
        'students_activities:update',
        'students_qualifications:view',
        'students_awards:view',

        # Courses (full academic control except delete)
        'courses_courses:view','courses_courses:create','courses_courses:update',
        'courses_subjects:view','courses_subjects:create','courses_subjects:update',
        'courses_modules:view','courses_modules:create','courses_modules:update',
        'courses_syllabus:view','courses_syllabus:create','courses_syllabus:update',
        'courses_detail_syllabus:view','courses_detail_syllabus:create','courses_detail_syllabus:update',
        'courses_batches:view','courses_batches:create','courses_batches:update',

        # Self account
        'self_account:update','self_account:create',

            
        # Self Permission 
        'rbac_permissions_self:view'
    ],
}



